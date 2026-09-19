Source: https://docs.typesafe.ai/sdk/javascript/api/interfaces/SystemOneResult
Retrieved: 2026-09-17T22:21:37.872885+00:00

# Interface: SystemOneResult<Q>

Answers keyed by question name, with model and usage metadata.

## Type Parameters

### Q

`Q` *extends* [`Questions`](Questions.md)

## Properties



### answers

```ts theme={null}
readonly answers: { readonly [K in string | number | symbol]: ResultFor<Q[K]> };
```

Answers with types inferred from the supplied questions.

***



### model

```ts theme={null}
readonly model: string;
```

The model used to answer the request.

***



### usage

```ts theme={null}
readonly usage: Usage;
```

Token usage for the request.
