Source: https://docs.typesafe.ai/sdk/javascript/api/interfaces/ChoiceQuestion
Retrieved: 2026-09-17T22:21:37.872885+00:00

# Interface: ChoiceQuestion<T>

A question that selects between named alternatives.

## Type Parameters

### T

`T` *extends* [`ChoiceCriteria`](../type-aliases/ChoiceCriteria.md) = [`ChoiceCriteria`](../type-aliases/ChoiceCriteria.md)

## Properties



### criteria

```ts theme={null}
criteria: T;
```

Descriptions of the available outcomes.

***



### instructions?

```ts theme={null}
optional instructions?: EntryType;
```

The question as text, a JSON object, or an array; optional or `null`.

***



### type

```ts theme={null}
type: "choice";
```
