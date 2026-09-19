Source: https://docs.typesafe.ai/sdk/javascript/api/type-aliases/EntryType
Retrieved: 2026-09-17T22:21:37.872885+00:00

# Type Alias: EntryType

```ts theme={null}
type EntryType = 
  | string
  | {
[key: string]: JsonValue;
}
  | JsonValue[]
  | null;
```

Text, a JSON object or array, or `null` for state, instructions, and criteria.
