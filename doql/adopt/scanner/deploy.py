"""Deployment scanning — Docker, docker-compose, quadlet, ansible, k8s, terraform, nginx."""
from __future__ import annotations

from pathlib import Path
from typing import Any

from ...parsers.models import DoqlSpec, Deploy, Infrastructure, Ingress
from .utils import find_compose, find_dockerfiles, load_yaml, walk_files


# Database images to skip when extracting containers
_DB_IMAGES = ("postgres", "mysql", "redis", "mongo")


def _detect_deployment_indicators(root: Path) -> dict[str, Any]:
    """Detect deployment infrastructure indicators."""
    return {
        "compose": find_compose(root),
        "has_dockerfile": bool(find_dockerfiles(root)),
        "has_quadlet": (root / "infra" / "quadlet").is_dir() or
                       (root / "deploy" / "quadlet").is_dir(),
        "has_ansible": any((root / d).is_dir()
                          for d in ("ansible", "deploy/ansible", "infra/ansible")),
        "has_makefile": (root / "Makefile").exists(),
        "has_k8s": any(
            f.name.startswith(("deployment", "service", "ingress", "configmap", "kustomization"))
            for f in walk_files(root, extensions=(".yaml", ".yml"))
        ),
        "has_terraform": (root / "main.tf").exists()
                         or (root / "infra" / "main.tf").exists()
                         or (root / "terraform" / "main.tf").exists(),
        "has_nginx": (root / "nginx.conf").exists()
                      or (root / "infra" / "nginx.conf").exists(),
        "has_vite": (root / "vite.config.ts").exists()
                     or (root / "vite.config.js").exists()
                     or (root / "vite.config.mjs").exists(),
        "has_doql_plugins": (root / ".doql-plugins").is_dir(),
    }


def _determine_deploy_target(indicators: dict[str, Any], deploy: Deploy, root: Path) -> None:
    """Set deployment target based on detected indicators."""
    compose = indicators["compose"]
    if compose:
        deploy.target = "docker-compose"
        deploy.config["compose_file"] = str(compose.relative_to(root))
    elif indicators["has_dockerfile"]:
        deploy.target = "docker"
    elif indicators["has_quadlet"]:
        deploy.target = "podman-quadlet"
    elif indicators["has_k8s"]:
        deploy.target = "kubernetes"
    elif indicators["has_terraform"]:
        deploy.target = "terraform"
    elif indicators["has_makefile"]:
        deploy.target = "makefile"
    elif (root / "pyproject.toml").exists():
        deploy.target = "pip"


def _apply_deploy_config_flags(indicators: dict[str, Any], deploy: Deploy) -> None:
    """Apply boolean config flags based on indicators."""
    if indicators["has_quadlet"]:
        deploy.config["quadlet"] = True
    if indicators["has_ansible"]:
        deploy.config["ansible"] = True


def _is_database_service(image: str) -> bool:
    """Check if service image is a known database."""
    return any(db in image for db in _DB_IMAGES)


def _extract_container_config(svc_name: str, svc: dict[str, Any]) -> dict[str, Any]:
    """Extract container configuration from compose service."""
    image = svc.get("image", "")
    build = svc.get("build")
    ports = svc.get("ports", [])

    container: dict[str, Any] = {"name": svc_name}
    if image:
        container["image"] = image
    if build:
        container["build"] = build if isinstance(build, str) else build.get("context", ".")
    if ports:
        container["ports"] = ports
    return container


def _extract_containers_from_compose(compose: Path | None, deploy: Deploy) -> None:
    """Extract non-database containers from docker-compose."""
    if not compose:
        return

    data = load_yaml(compose)
    if not data:
        return

    services = data.get("services", {})
    for svc_name, svc in services.items():
        image = svc.get("image", "")
        if _is_database_service(image):
            continue
        container = _extract_container_config(svc_name, svc)
        deploy.containers.append(container)


def _detect_rootless(spec: DoqlSpec) -> bool:
    """Detect rootless podman from env refs."""
    return any("ROOTLESS" in ref.upper() for ref in spec.env_refs)


def _emit_infrastructure_blocks(indicators: dict[str, Any], spec: DoqlSpec) -> None:
    """Emit Infrastructure and Ingress blocks from detected files."""
    if indicators["has_k8s"]:
        spec.infrastructures.append(Infrastructure(
            name="k8s", type="kubernetes", provider="k3s"
        ))
    if indicators["has_terraform"]:
        spec.infrastructures.append(Infrastructure(
            name="tf", type="terraform", provider="docker"
        ))
    if indicators["has_nginx"]:
        spec.ingresses.append(Ingress(
            name="nginx", type="nginx", tls=False
        ))


def scan_deploy(root: Path, spec: DoqlSpec) -> None:
    """Detect deployment infrastructure."""
    indicators = _detect_deployment_indicators(root)
    deploy = Deploy()

    _determine_deploy_target(indicators, deploy, root)
    _apply_deploy_config_flags(indicators, deploy)

    if _detect_rootless(spec):
        deploy.rootless = True

    _extract_containers_from_compose(indicators["compose"], deploy)
    _emit_infrastructure_blocks(indicators, spec)

    spec.deploy = deploy

    # Override environment runtime for Python pip/makefile projects without compose
    compose_file = deploy.config.get("compose_file")
    if deploy.target in {"pip", "makefile"} and not compose_file:
        for env in spec.environments:
            if env.runtime in {"", "docker-compose"}:
                env.runtime = "python"
