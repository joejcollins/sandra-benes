import marimo

__generated_with = "0.14.17"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""# Tests""")
    return


@app.cell
def _():
    """Dummy helper demonstration."""
    from sandra_benes import dummy_helper

    new_number = dummy_helper.add_things(1, 2)

    print(new_number)


    return


if __name__ == "__main__":
    app.run()
