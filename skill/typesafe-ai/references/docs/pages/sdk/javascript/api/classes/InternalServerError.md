Source: https://docs.typesafe.ai/sdk/javascript/api/classes/InternalServerError
Retrieved: 2026-09-17T22:21:37.872885+00:00

# Class: InternalServerError

HTTP 5xx: the server failed to handle the request.

## Extends

* [`APIError`](APIError.md)

## Constructors



### Constructor

```ts theme={null}
new InternalServerError(
   status, 
   body, 
   headers, 
   message?
): InternalServerError;
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

`InternalServerError`

#### Inherited from

[`APIError`](APIError.md).[`constructor`](APIError.md#sdk-constructor)

## Properties



### body

```ts theme={null}
readonly body: unknown;
```

Parsed JSON, response text, or `undefined` for an empty body.

#### Inherited from

[`APIError`](APIError.md).[`body`](APIError.md#sdk-body)

***



### headers

```ts theme={null}
readonly headers: Headers;
```

HTTP response headers.

#### Inherited from

[`APIError`](APIError.md).[`headers`](APIError.md#sdk-headers)

***



### requestId

```ts theme={null}
readonly requestId: string | undefined;
```

Request ID from `x-typesafe-request-id`, or `undefined` when absent.

#### Inherited from

[`APIError`](APIError.md).[`requestId`](APIError.md#sdk-requestid)

***



### status

```ts theme={null}
readonly status: number;
```

HTTP response status code.

#### Inherited from

[`APIError`](APIError.md).[`status`](APIError.md#sdk-status)

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

[`APIError`](APIError.md)

#### Inherited from

[`APIError`](APIError.md).[`fromResponse`](APIError.md#sdk-fromresponse)
