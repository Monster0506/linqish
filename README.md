# Linqish

Linqish is a small query helper for Python collections and iterables.

It provides a fluent interface for filtering, transforming, grouping, and aggregating data while remaining compatible with arbitrary iterables.

```python
from linqish import Find

active_names = (
    Find(users)
    .thatAre(lambda user: user.active)
    .without(lambda user: user.banned)
    .mappedTo(lambda user: user.name)
    .withoutDuplicates()
    .orderedBy(str.lower)
    .toList()
)
```

## Design

Linqish is intentionally small.

* Works with any iterable
* Most query operations are lazy
* Uses Python callables rather than a custom expression language
* Favors readable method chaining over nested calls

The API is loosely inspired by LINQ while using more natural method names.

## Querying

### Filtering

```python
adults = (
    Find(people)
    .thatAre(lambda p: p.age >= 18)
)

verified_adults = (
    Find(people)
    .thatAre(is_adult)
    .andAre(is_verified)
)

admins_or_moderators = (
    Find(users)
    .thatAre(is_admin)
    .orAre(is_moderator)
)

visible_users = (
    Find(users)
    .without(is_banned)
)
```

### Mapping

```python
emails = (
    Find(users)
    .mappedTo(lambda user: user.email)
)
```

### Flattening

```python
all_tags = (
    Find(posts)
    .expandedTo(lambda post: post.tags)
)
```

### Distinct Values

```python
unique_names = (
    Find(users)
    .mappedTo(lambda user: user.name)
    .withoutDuplicates()
)
```

```python
unique_users = (
    Find(users)
    .distinctBy(lambda user: user.id)
)
```

### Ordering

```python
ordered = (
    Find(users)
    .orderedBy(lambda user: user.last_name)
)
```

### Grouping

```python
groups = (
    Find(users)
    .groupedBy(lambda user: user.department)
)

for department, users in groups:
    ...
```

## Aggregation

### First

```python
first_user = Find(users).first()
```

### Count

```python
user_count = Find(users).count()
```

### Any

```python
has_users = Find(users).hasAny()
```

### All

```python
all_active = (
    Find(users)
    .areAll(lambda user: user.active)
)
```

### Materialization

```python
user_list = Find(users).toList()
```

## Side Effects

`then()` allows an operation to observe the current query before continuing.

```python
(
    Find(users)
    .thatAre(is_active)
    .then(lambda users: print(users.count()))
    .mappedTo(lambda user: user.name)
)
```

## Notes

* `orderedBy()` materializes the sequence in order to sort it.
* `withoutDuplicates()` requires elements to be hashable.
* `distinctBy()` requires the selected key to be hashable.
* `groupedBy()` preserves the insertion order of groups.
