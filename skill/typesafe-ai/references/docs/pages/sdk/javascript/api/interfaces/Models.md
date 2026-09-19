Source: https://docs.typesafe.ai/sdk/javascript/api/interfaces/Models
Retrieved: 2026-09-17T22:21:37.872885+00:00

# Interface: Models

Access to the Models API resource.

## Methods



### list()

```ts theme={null}
list(options?): APIPromise<ModelCard[]>;
```

List the models available to the account.

#### Parameters

##### options?

[`RequestOptions`](RequestOptions.md) = `{}`

#### Returns

[`APIPromise`](../classes/APIPromise.md)\<[`ModelCard`](ModelCard.md)\[]>
