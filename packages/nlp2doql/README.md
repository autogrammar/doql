# nlp2doql

Sterowanie manifestami DOQL przez **język naturalny** — generacja, walidacja, edycja (via nlp2uri → uri2doql).

Powiązane: [indeks paczek](../README.md) · [README główne doql](../../README.md) · [uri2doql](../uri2doql/README.md)

## Do czego służy

- **generate** — NL → pełny `.doql.less` (reguły lub centralne SubLLM)
- **validate** — walidacja pliku DOQL
- **apply** — NL → intent (query/patch/materialize/generate) + wykonanie
- **edit** — NL + plik fragmentu → patch bloku

## CLI

```bash
nlp2doql generate "CRM z kontaktami" --out app.doql.less --validate
nlp2doql validate app.doql.less
nlp2doql apply "pokaż app metadata" --file app.doql.less
nlp2doql edit "update entity Contact" --file app.doql.less --with contact.patch.less
nlp2doql apply "validate app.doql.less"
```

## Kontrakt odpowiedzi LLM

Plan zwracany przez model jest kontraktem `DoqlPlan 1.0.0`, a nie swobodnym
fragmentem tekstu. Pakiet publikuje równoważne artefakty w
`nlp2doql/contracts/v1`: gramatykę GBNF, model Protobuf, JSON Schema oraz
manifest wiążący je z `nlp2doql.llm.plan_with_subllm`.

Przy użyciu `nlp2doql[llm]` JSON Schema jest przekazywany do SubLLM
(`autogrammar-doql/translate`) jako `response_format` i ponownie sprawdzany
lokalnie przed utworzeniem DOQL. Wybór providera i modelu należy do SubLLM.
Błędna wersja kontraktu, tekst otaczający JSON, brak bloków albo niezgodne
typy kończą generowanie błędem zamiast uruchamiać cichy fallback.

## Testy

```bash
pytest packages/nlp2doql/tests -q
```
