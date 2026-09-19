Source: https://docs.typesafe.ai/sdk/javascript/api/classes/APIError
Retrieved: 2026-09-17T22:21:37.872885+00:00

# Class: APIError

An unsuccessful HTTP response from the API.

## Extends

* [`TypeSafeError`](TypeSafeError.md)

## Extended by

* [`AuthenticationError`](AuthenticationError.md)
* [`BadRequestError`](BadRequestError.md)
* [`InternalServerError`](InternalServerError.md)
* [`NotFoundError`](NotFoundError.md)
* [`PermissionDeniedError`](PermissionDeniedError.md)
* [`RateLimitError`](RateLimitError.md)
* [`UnprocessableEntityError`](UnprocessableEntityError.md)

## Constructors



### Constructor

```ts theme={null}
new APIError(
   status, 
   body, 
   headers, 
   message?
): APIError;
```

#### Parameters

##### status

`number`

##### body

`unknown`

##### headers

`Headers`

##### message?

`string`

#### Returns

`APIError`

#### Overrides

[`TypeSafeError`](TypeSafeError.md).[`constructor`](TypeSafeError.md#sdk-constructor)

## Properties



### body

```ts theme={null}
readonly body: unknown;
```

Parsed JSON, response text, or `undefined` for an empty body.

***



### headers

```ts theme={null}
readonly headers: Headers;
```

HTTP response headers.

***



### requestId

```ts theme={null}
readonly requestId: string | undefined;
```

Request ID from `x-typesafe-request-id`, or `undefined` when absent.

***



### status

```ts theme={null}
readonly status: number;
```

HTTP response status code.

## Methods



### fromResponse()

```ts theme={null}
static fromResponse(
   status, 
   body, 
   headers
): APIError;
```

Create the error subclass for an HTTP status code.

#### Parameters

##### status

`number`

##### body

`unknown`

##### headers

`Headers`

#### Returns

`APIError`
