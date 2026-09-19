Source: https://docs.typesafe.ai/sdk/javascript/api/interfaces/ScoreQuestion
Retrieved: 2026-09-17T22:21:37.872885+00:00

# Interface: ScoreQuestion<T>

A question that assigns a score using an ordered rubric.

## Type Parameters

### T

`T` *extends* [`ScoreCriteria`](../type-aliases/ScoreCriteria.md) = [`ScoreCriteria`](../type-aliases/ScoreCriteria.md)

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
type: "score";
```
