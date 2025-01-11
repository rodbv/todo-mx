[![Django CI](https://github.com/rodbv/todo-mx/actions/workflows/django.yml/badge.svg)](https://github.com/rodbv/todo-mx/actions/workflows/django.yml)


# TodoMX

This repository is associated with a series of articles on [dev.to](https://dev.to/rodbv/series/30050) documenting my learning journey with [HTMX](https://htmx.org/) and [Django](https://www.djangoproject.com/). The series covers the creation of a to-do application, using [uv](https://docs.astral.sh/uv/), [DaisyUI](https://daisyui.com/) and [Pytest](https://docs.pytest.org/en/stable/).

## Articles in the Series

The series is being published in dev.to: https://dev.to/rodbv/series/30050

## Technologies Used

- **Django**: A high-level Python web framework that encourages rapid development and clean, pragmatic design.
- **HTMX**: A library that allows you to access modern browser features directly from HTML, making it easier to build dynamic web applications.
- **pytest**: A framework that makes building simple and scalable test cases easy.

## Getting Started

To get started with this project, clone the repository and install the dependencies:

```sh
git clone https://github.com/yourusername/todomx.git
cd todomx
uv sync
```

## Running Tests

To run the tests, use the following command:

```sh
uv run pytest
```

## Using Justfile Commands

This project uses `just` to manage common tasks. To install `just`, follow the instructions on their [official website](https://just.systems/).

Here are some of the available commands:

- **Run the development server**:
  ```sh
  just run
  ```

- **Run tests**:
  ```sh
  just test
  ```

- **Apply database migrations**:
  ```sh
  just migrate
  ```

- **Create a superuser**:
  ```sh
  just csu
  ```

- **Make database migrations**:
  ```sh
  just makemigrations
  ```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

