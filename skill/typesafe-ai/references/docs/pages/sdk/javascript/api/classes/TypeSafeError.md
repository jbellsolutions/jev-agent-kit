Source: https://docs.typesafe.ai/sdk/javascript/api/classes/TypeSafeError
Retrieved: 2026-09-17T22:21:37.872885+00:00

# Class: TypeSafeError

Base class for SDK errors.

## Extends

* `Error`

## Extended by

* [`APIConnectionError`](APIConnectionError.md)
* [`APIError`](APIError.md)
* [`APIUserAbortError`](APIUserAbortError.md)

## Constructors



### Constructor

```ts theme={null}
new TypeSafeError(message, options?): TypeSafeError;
```

#### Parameters

##### message

`string`

##### options?

`ErrorOptions`

#### Returns

`TypeSafeError`

#### Overrides

```ts theme={null}
Error.constructor
```
