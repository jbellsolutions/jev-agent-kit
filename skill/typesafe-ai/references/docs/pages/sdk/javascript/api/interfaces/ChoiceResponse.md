Source: https://docs.typesafe.ai/sdk/javascript/api/interfaces/ChoiceResponse
Retrieved: 2026-09-17T22:21:37.872885+00:00

# Interface: ChoiceResponse<T>

A selected label and its probabilities.

## Type Parameters

### T

`T` *extends* [`ChoiceCriteria`](../type-aliases/ChoiceCriteria.md) = [`ChoiceCriteria`](../type-aliases/ChoiceCriteria.md)

## Properties



### choice

```ts theme={null}
readonly choice: keyof T & string;
```

The selected label.

***



### confidence

```ts theme={null}
readonly confidence: number;
```

Reported confidence in the selected label.

***



### probabilities

```ts theme={null}
readonly probabilities: { readonly [label in string | number | symbol]: number };
```

Probabilities keyed by label.

***



### type

```ts theme={null}
readonly type: "choice";
```
