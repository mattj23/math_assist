"""
    This script shows examples of the different ways to output the working history of an equation or expression. There
    are different reasons to use the different methods, and the following code will try to show what the advantages
    and disadvantages of each method are.
"""

import sympy
from math_assist import Expression
from math_assist.output import Markdown


def main():
    x = sympy.symbols("x")
    exp = Expression(x**2 + 2*x + 1)

    # ================================================================================================================
    # The first example is the simplest way to use the math output.  We will manually declare an output, manually add
    # text to it, and then manually save it to a file.  This is not likely to be the best method for most use cases,
    # but it does show how to use the output object directly.
    # ================================================================================================================

    # First we declare the output object. We could give it a `file_name` argument which would allow it to write to file
    # later without needing to specify a name.
    output = Markdown()

    # The output object is callable like the print function, and when called it will add text to the output. Arguments
    # which are `str` types will be added as text, everything else will try to be converted to Latex. Here we add a
    # line of text followed by the Latex rendered version of the expression.
    output("Initial expression:")
    output(exp)

    # In this step we do two operations before printing the result to the output. By manually adding text to the output
    # in this way we can control when we want to display the result of operations and when we want to skip them.
    output("Multiply by $x^3 + 2x$ and expand:")
    exp.multiply_by(x**3 + 2*x)
    exp.expand()
    output(exp)

    output("Factor the expression:")
    exp.factor()
    output(exp)

    # The output object has a `write` method which will save the output to a file.  If the output object was created
    # with a `file_name` argument, then the `write` method will use that name if no argument is given. Otherwise, the
    # `write` method will preferentially use the argument given to it.
    output.write("temp.md")

    # ================================================================================================================
    # This second example shows us how to use the context manager to save the file when the context is exited. This is
    # useful when you want to make sure that the file gets saved up to the current point in the code even if an error
    # occurs.
    # ================================================================================================================
    exp = Expression(x**2 + 2*x + 1)

    # In this case, we will need to specify the file name when we create the output object, because the context manager
    # won't get the chance to ask for it later.
    with Markdown(file_name="temp.md") as output:
        output("Initial expression:")
        output(exp)

        output("Multiply by $x^3 + 2x$ and expand:")
        exp.multiply_by(x**3 + 2*x)
        exp.expand()
        output(exp)

        output("Factor the expression:")
        exp.factor()
        output(exp)

    # ================================================================================================================
    # This third example shows how to use the `write_all_to` method to write the history of the expression to the
    # output at the end of a set of operations. This uses the internal history of the expression to decide what to
    # send to the output, and does not require you to manually add text to the output.  However, it does not allow you
    # to control which steps are shown and which are not.
    # ================================================================================================================
    exp = Expression(x**2 + 2*x + 1)
    exp.multiply_by(x ** 3 + 2 * x)
    exp.expand()
    exp.factor()

    # This can be done with or without the context manager
    with Markdown(file_name="temp.md") as output:
        # There is an optional argument to specify if you want to skip writing the initial state of the first step in
        # the history, which can be done with `skip_start_state=True`.
        exp.write_history_to(output)

    # ================================================================================================================
    # This fourth example shows how to attach an output object to an expression or equation so that the history of
    # operations is written to the output as they are done. This is most useful when used with the context manager.
    # ================================================================================================================
    exp = Expression(x**2 + 2*x + 1)

    with Markdown(file_name="temp.md") as output:
        # When we attach the output object to the expression, the initial state of the expression is written to the
        # output automatically.  This can be skipped with the `skip_start_state` argument.
        exp.attach_output(output)

        # Now, as we do operations on the expression, the history of the operations will be written to the output.
        exp.multiply_by(x ** 3 + 2 * x)
        exp.expand()
        exp.factor()

        # We can detach the output object from the expression at any time, which will stop the history from being
        # written to the output.
        exp.detach_output(output)


if __name__ == "__main__":
    main()



