Source: https://docs.typesafe.ai/sdk/javascript/api/type-aliases/JsonValue
Retrieved: 2026-09-17T22:21:37.872885+00:00

# Type Alias: JsonValue

```ts theme={null}
type JsonValue = 
  | string
  | number
  | boolean
  | null
  | JsonValue[]
  | {
[key: string]: JsonValue;
};
```

A JSON-compatible value.
