Source: https://docs.typesafe.ai/sdk/javascript/api/type-aliases/ScoreOf
Retrieved: 2026-09-17T22:21:37.872885+00:00

# Type Alias: ScoreOf<T>

```ts theme={null}
type ScoreOf<T> = number extends T["length"] ? number : Extract<keyof T, `${number}`>;
```

Score keys inferred from the rubric; a fixed-length tuple yields its indices, otherwise `number`.

## Type Parameters

### T

`T` *extends* [`ScoreCriteria`](ScoreCriteria.md)
