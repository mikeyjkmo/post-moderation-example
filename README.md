# Post Moderation ML Example

## Requirements

- Python3.9 or above
- Python Poetry

## Installation

```bash
> poetry install
```

## Run Tests

```bash
make test
```

## Future Improvements

- The method used to split `Post` paragraphs into sentences is extremely naive in
  this implementation. With more time I would use `ntlk` to tokenize the
  paragraph appropriately.
- Ideally, if the requirement is the always allow the `Post` to be persisted prior
  to moderation, I would use an event-driven system to achieve this (using a messaging
  queue like `Kafka`). An event would be dispatched when a `Post` has been created,
  say `PostCreated`. This event would be acted upon by a background consumer.
