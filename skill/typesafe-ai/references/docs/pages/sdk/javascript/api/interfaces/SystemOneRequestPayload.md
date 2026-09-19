Source: https://docs.typesafe.ai/sdk/javascript/api/interfaces/SystemOneRequestPayload
Retrieved: 2026-09-17T22:21:37.872885+00:00

# Interface: SystemOneRequestPayload

Request body for `POST /v1/systemone`, with the model resolved.

## Extends

* [`SystemOneRequest`](SystemOneRequest.md)

## Properties



### model

```ts theme={null}
model: string;
```

Model override; omitted values inherit `defaultModel`.

#### Overrides

[`SystemOneRequest`](SystemOneRequest.md).[`model`](SystemOneRequest.md#sdk-model)

***



### questions

```ts theme={null}
questions: Questions;
```

Nonempty questions keyed by the names used to identify their answers.

#### Inherited from

[`SystemOneRequest`](SystemOneRequest.md).[`questions`](SystemOneRequest.md#sdk-questions)

***



### state

```ts theme={null}
state: EntryType;
```

Text, a JSON object or array, or `null` to evaluate.

#### Inherited from

[`SystemOneRequest`](SystemOneRequest.md).[`state`](SystemOneRequest.md#sdk-state)
