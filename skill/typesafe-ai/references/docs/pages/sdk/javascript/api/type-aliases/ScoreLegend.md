Source: https://docs.typesafe.ai/sdk/javascript/api/type-aliases/ScoreLegend
Retrieved: 2026-09-17T22:21:37.872885+00:00

# Type Alias: ScoreLegend<T>

```ts theme={null}
type ScoreLegend<T> = { readonly [score in ScoreOf<T>]: T[score] };
```

Rubric descriptions keyed by score.

## Type Parameters

### T

`T` *extends* [`ScoreCriteria`](ScoreCriteria.md)
