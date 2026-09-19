Source: https://docs.typesafe.ai/sdk/javascript/api/interfaces/ScoreResponse
Retrieved: 2026-09-17T22:21:37.872885+00:00

# Interface: ScoreResponse<T>

An expected score with its rubric and probabilities.

## Type Parameters

### T

`T` *extends* [`ScoreCriteria`](../type-aliases/ScoreCriteria.md) = [`ScoreCriteria`](../type-aliases/ScoreCriteria.md)

## Properties



### confidence

```ts theme={null}
readonly confidence: number;
```

Reported confidence in the score.

***



### legend

```ts theme={null}
readonly legend: ScoreLegend<T>;
```

Rubric descriptions keyed by score.

***



### probabilities

```ts theme={null}
readonly probabilities: { readonly [score in number | `${number}`]: number };
```

Probabilities keyed by score.

***



### score

```ts theme={null}
readonly score: number;
```

Expected score, which may fall between integer rubric levels.

***



### type

```ts theme={null}
readonly type: "score";
```
