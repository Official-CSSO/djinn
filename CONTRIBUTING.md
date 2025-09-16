## Contributing Guidelines
This section is all about guidelines & information before contributing. Please follow 'em :)
<br />
### Introduction
Before you start, [you need to create your own test bot](https://discord.com/developers). Then create .env file using the [.env.example](https://github.com/Official-CSSO/djinn/blob/master/.env.example) by replacing ***your own bot token***.

- The bot is tested with [Python 3.13](https://www.python.org/downloads/release/python-3137/)
- It is suggested to use virtualenv. [Check this for more information](https://docs.python.org/3/library/venv.html).

## Conventional Commit Guidelines
I use simple commit messages to make things simpler and organized. Please refer:

> [!NOTE]
> You can also add a **scope** in each commit message.  
> e.g `fix(trivia): only the author can use this interaction`
>  
> `<type>(<scope>): <short description>`

> [!TIP]
> Make sure to include `!` if you have *breaking changes*  
> which means something that is not backward compatible. `feat!: switch to discord.py v3`

- `feat`: – if you added a new feature.
- `fix`: – if you fixed a bug.
- `ref`: – if you changed code structure without changing functionality (e.g., cleaning, reorganizing).
- `perf`: – if you improved performance.
- `style`: – if you only changed formatting (no logic, e.g., indentation, spacing).
- `docs`: – if you updated only documentation.
- `test`: – if you added or changed tests.
- `chore`: – if you updated build tools, configs, or maintenance stuff.

