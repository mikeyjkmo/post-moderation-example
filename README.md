# Post Moderation Example

## Design

This is a simple FastAPI CRUD app with a background task that periodically
moderates any unmoderated posts. The default interval for this background task
is 10 seconds. If an error occurs during an iteration, the task will continue
to try again on the next interval.

- When a `Post` is initially created, it will be unmoderated and will not
  have a value for `has_foul_language`.
- The background task will process all unmoderated posts on each iteration
  and set the `has_foul_language` field appropriately based on the result from
  the Content Moderation service.

NOTE: As mentioned in the **Future Improvements** section below, this
is not how I would ideally implement something like this in a production environment.

## Requirements

- Python3.9 or above
- Python Poetry

## Installation

```bash
> poetry install
```

## Run Tests

```bash
> make test
```

## Running The Development Server

```bash
>  make develop
```

Navigate to `http://localhost:8000/docs` to test the API out.

## Future Improvements

- The method used to split `Post` paragraphs into sentences is extremely naive in
  this implementation. With more time I would use `ntlk` to tokenize the
  paragraph appropriately.
- Ideally, if the requirement is the always allow the `Post` to be persisted prior
  to moderation, I would use an event-driven system to achieve this (using a messaging
  queue like `Kafka`). An event would be dispatched when a `Post` has been created,
  say `PostCreated`. This event would be acted upon by a background consumer. Consumers
  would only commit their offsets after successfully moderating a created/updated `Post`.
