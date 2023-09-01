"""
Simplified VM code which works for some cases.
You need extend/rewrite code to pass all cases.
"""

import builtins
import dis
import types
import typing as tp


class Frame:
    """
    Frame header in cpython with description
        https://github.com/python/cpython/blob/3.10/Include/frameobject.h

    Text description of frame parameters
        https://docs.python.org/3/library/inspect.html?highlight=frame#types-and-members
    """
    def __init__(self,
                 frame_code: types.CodeType,
                 frame_builtins: dict[str, tp.Any],
                 frame_globals: dict[str, tp.Any],
                 frame_locals: dict[str, tp.Any]) -> None:
        self.offset = 0
        self.code = frame_code
        self.builtins = frame_builtins
        self.globals = frame_globals
        self.locals = frame_locals
        self.data_stack: tp.Any = []
        self.return_value = None

    def top(self) -> tp.Any:
        return self.data_stack[-1]

    def pop(self) -> tp.Any:
        return self.data_stack.pop()

    def push(self, *values: tp.Any) -> None:
        self.data_stack.extend(values)

    def popn(self, n: int) -> tp.Any:
        """
        Pop a number of values from the value stack.
        A list of n values is returned, the deepest value first.
        """
        if n > 0:
            returned = self.data_stack[-n:]
            self.data_stack[-n:] = []
            return returned
        else:
            return []

    def run(self) -> tp.Any:
        instructions = list(dis.get_instructions(self.code))
        i = 0
        while i < len(instructions):
            instruction = instructions[i]
            self.offset += 2
            getattr(self, instruction.opname.lower() + "_op")(instruction.argval)

            if self.offset != instruction.offset + 2 or "jump" in instruction.opname.lower():
                for ins in instructions:
                    if ins.offset == self.offset:
                        i = instructions.index(ins)
                        break
            else:
                i += 1

        return self.return_value

    def call_function_op(self, arg: int) -> None:
        """
        Operation description:
            https://docs.python.org/release/3.10.6/library/dis.html#opcode-CALL_FUNCTION

        Operation realization:
            https://github.com/python/cpython/blob/3.10/Python/ceval.c#4243
        """
        arguments = self.popn(arg)
        f = self.pop()
        self.push(f(*arguments))

    def load_name_op(self, arg: str) -> None:
        """
        Partial realization

        Operation description:
            https://docs.python.org/release/3.10.6/library/dis.html#opcode-LOAD_NAME

        Operation realization:
            https://github.com/python/cpython/blob/3.10/Python/ceval.c#L2829
        """
        # TODO: parse all scopes
        if arg in self.locals:
            self.push(self.locals[arg])
        elif arg in self.builtins:
            self.push(self.builtins[arg])
        elif arg in self.globals:
            self.push(self.globals[arg])
        else:
            raise NameError

    def load_global_op(self, arg: str) -> None:
        """
        Operation description:
            https://docs.python.org/release/3.10.6/library/dis.html#opcode-LOAD_GLOBAL

        Operation realization:
            https://github.com/python/cpython/blob/3.10/Python/ceval.c#L2958
        """
        # TODO: parse all scopes
        if arg in self.globals:
            self.push(self.globals[arg])
        elif arg in self.builtins:
            self.push(self.builtins[arg])
        else:
            raise NameError

    def load_const_op(self, arg: tp.Any) -> None:
        """
        Operation description:
            https://docs.python.org/release/3.10.6/library/dis.html#opcode-LOAD_CONST

        Operation realization:
            https://github.com/python/cpython/blob/3.10/Python/ceval.c#L1871
        """
        self.push(arg)

    def return_value_op(self, arg: tp.Any) -> None:
        """
        Operation description:
            https://docs.python.org/release/3.10.6/library/dis.html#opcode-RETURN_VALUE

        Operation realization:
            https://github.com/python/cpython/blob/3.10/Python/ceval.c#L2436
        """
        self.return_value = self.pop()

    def pop_top_op(self, arg: tp.Any) -> None:
        """
        Operation description:
            https://docs.python.org/release/3.10.6/library/dis.html#opcode-POP_TOP

        Operation realization:
            https://github.com/python/cpython/blob/3.10/Python/ceval.c#L1886
        """
        self.pop()

    def make_function_op(self, arg: int) -> None:
        """
        Operation description:
            https://docs.python.org/release/3.10.6/library/dis.html#opcode-MAKE_FUNCTION

        Operation realization:
            https://github.com/python/cpython/blob/3.10/Python/ceval.c#L4290

        Parse stack:
            https://github.com/python/cpython/blob/3.10/Objects/call.c#L612

        Call function in cpython:
            https://github.com/python/cpython/blob/3.10/Python/ceval.c#L4209
        """
        self.pop()
        code = self.pop()

        posonlyargcount = code.co_posonlyargcount
        kwonlyargcount = code.co_kwonlyargcount
        argcount = code.co_argcount
        is_args = 4 == 4 & code.co_flags
        is_kwargs = 8 == 8 & code.co_flags
        kw_only_dict = self.pop() if 0x02 == arg & 0x02 else {}
        pos_only_tuple = self.pop() if 0x01 == arg & 0x01 else ()

        def f(*args: tp.Any, **kwargs: tp.Any) -> tp.Any:
            # TODO: parse input arguments using code attributes such as co_argcount
            pos_args = code.co_varnames[0: posonlyargcount]
            usual_args = code.co_varnames[posonlyargcount: argcount]
            kw_args = code.co_varnames[argcount: argcount + kwonlyargcount]
            default_args = dict(zip(reversed(pos_args + usual_args), reversed(pos_only_tuple)))

            parsed_args: tp.Dict[str, tp.Any] = {}
            args_ind = kwonlyargcount + argcount
            args_list = list(args)
            for arg in pos_args:
                if len(args_list):
                    parsed_args[arg] = args_list.pop(0)
                else:
                    parsed_args[arg] = default_args[arg]

            for arg in usual_args:
                if len(args_list):
                    parsed_args[arg] = args_list.pop(0)
                elif arg in kwargs.keys():
                    parsed_args[arg] = kwargs[arg]
                    del kwargs[arg]
                else:
                    parsed_args[arg] = default_args[arg]

            if is_args:
                var = code.co_varnames[args_ind]
                if var not in parsed_args.keys():
                    parsed_args[var] = tuple(args_list)
            for arg in kw_args:
                if arg not in kwargs.keys():
                    parsed_args[arg] = kw_only_dict[arg]
                    continue
                parsed_args[arg] = kwargs[arg]
                del kwargs[arg]

            if is_kwargs:
                kwargs_name = code.co_varnames[args_ind + 1] if is_args else code.co_varnames[args_ind]
                if kwargs_name not in parsed_args.keys():
                    parsed_args[kwargs_name] = kwargs

            f_locals = dict(self.locals)
            f_locals.update(parsed_args)

            frame = Frame(code, self.builtins, self.globals, f_locals)  # Run code in prepared environment
            return frame.run()

        self.push(f)

    def store_name_op(self, arg: str) -> None:
        """
        Operation description:
            https://docs.python.org/release/3.10.6/library/dis.html#opcode-STORE_NAME

        Operation realization:
            https://github.com/python/cpython/blob/3.10/Python/ceval.c#L2758
        """
        const = self.pop()
        self.locals[arg] = const

    def store_subscr_op(self, arg: str) -> None:
        tos2, tos1, tos0 = self.popn(3)
        tos1[tos0] = tos2
        self.push(tos1[tos0])

    def store_global_op(self, arg: str) -> None:
        const = self.pop()
        self.globals[arg] = const

    def load_fast_op(self, arg: str) -> None:
        if arg in self.locals:
            self.push(self.locals[arg])
        else:
            raise UnboundLocalError("")

    def store_fast_op(self, arg: str) -> None:
        self.locals[arg] = self.pop()

    def extended_arg_op(self, count: int) -> None:
        res = 0
        while count:
            count -= 1
            a = self.pop()
            res = (res << 8) | a
        self.push(res)

    def unpack_sequence_op(self, _: tp.Any) -> None:
        seq = self.pop()
        for x in reversed(seq):
            self.push(x)

    def binary_matrix_multiply(self) -> None:
        pass

    def binary_add_op(self, _: tp.Any) -> None:
        val1, val2 = self.popn(2)
        self.push(val1 + val2)

    def inplace_add_op(self, _: tp.Any) -> None:
        val1, val2 = self.popn(2)
        self.push(val1 + val2)

    def binary_modulo_op(self, _: tp.Any) -> None:
        val1, val2 = self.popn(2)
        self.push(val1 % val2)

    def binary_multiply_op(self, _: tp.Any) -> None:
        val1, val2 = self.popn(2)
        self.push(val1 * val2)

    def inplace_multiply_op(self, _: tp.Any) -> None:
        val1, val2 = self.popn(2)
        self.push(val1 * val2)

    def inplace_true_divide_op(self, _: tp.Any) -> None:
        val1, val2 = self.popn(2)
        self.push(val1 / val2)

    def binary_power_op(self, _: tp.Any) -> None:
        val1, val2 = self.popn(2)
        self.push(val1 ** val2)

    def binary_subscr_op(self, _: tp.Any) -> None:
        val1, val2 = self.popn(2)
        if not isinstance(val1, int):
            self.push(val1[val2])

    def delete_subscr_op(self, _: tp.Any) -> None:
        val1, val2 = self.popn(2)
        del val1[val2]
        self.push(val1)

    def jump_if_true_or_pop_op(self, off: int) -> None:
        val = self.pop()
        if val:
            self.push(val)
            self.offset = off

    def build_list_op(self, cnt: int) -> None:
        self.push(self.popn(cnt))

    def build_const_key_map_op(self, cnt: int) -> None:
        keys = self.pop()
        vals = self.popn(cnt)
        self.push(dict(zip(keys, vals)))

    def build_tuple_op(self, cnt: int) -> None:
        self.push(tuple(self.popn(cnt)))

    def build_slice_op(self, cnt: int) -> None:
        if cnt == 1:
            f = self.pop()
            self.push(slice(0, f))
        elif cnt == 2:
            b, f = self.popn(cnt)
            self.push(slice(b, f))
        elif cnt == 3:
            b, f, s = self.popn(cnt)
            self.push(slice(b, f, s))

    @staticmethod
    def compare_operations(op: str, v: tp.Any, w: tp.Any) -> bool:
        if op == '<':
            return v < w
        elif op == '<=':
            return v <= w
        elif op == '==':
            return v == w
        elif op == '!=':
            return v != w
        elif op == '>':
            return v > w
        else:
            return v >= w

    def compare_op_op(self, op: str) -> None:
        val1 = self.pop()
        val2 = self.pop()
        res = self.compare_operations(op, val2, val1)
        self.push(res)

    def unary_invert_op(self, _: tp.Any) -> None:
        self.push(~self.pop())

    def unary_negative_op(self, _: tp.Any) -> None:
        self.push(-self.pop())

    def unary_not_op(self, _: tp.Any) -> None:
        self.push(not self.pop())

    def call_function_kw_op(self, arg: int) -> None:
        kw_args = self.pop()
        args_list = self.popn(arg)
        ind = 0
        kw_op = {}

        while ind < len(kw_args):
            kw_op.update({kw_args[-ind - 1]: args_list[-ind - 1]})
            ind += 1

        func = self.pop()
        self.push(func(*args_list[:-ind], **kw_op))

    def dup_top_two_op(self, _: tp.Any) -> None:
        val1 = self.pop()
        val2 = self.pop()
        self.push(val2)
        self.push(val1)
        self.push(val2)
        self.push(val1)

    def rot_two_op(self, _: tp.Any) -> None:
        val1 = self.pop()
        val2 = self.pop()
        self.push(val1)
        self.push(val2)

    def rot_three_op(self, _: tp.Any) -> None:
        val1 = self.pop()
        val2 = self.pop()
        val3 = self.pop()
        self.push(val1)
        self.push(val3)
        self.push(val2)

    def get_iter_op(self, _: tp.Any) -> None:
        self.push(iter(self.pop()))

    def format_value_op(self, _: tp.Any) -> None:
        pass

    def build_map_op(self, cnt: int) -> None:
        arr = self.popn(2 * cnt)
        self.push(dict(zip(arr[::2], arr[1::2])))

    def load_method_op(self, val: str) -> None:
        obj = self.pop()
        obj_dict = obj.__class__.__dict__
        if val in obj_dict:
            self.push(obj)
            self.push(obj_dict[val])

    def call_method_op(self, arg: int) -> None:
        args = self.popn(arg)
        func = self.pop()
        obj = self.pop()
        self.push(func(obj, *args))

    def delete_name_op(self, val: str) -> None:
        del self.locals[val]

    def delete_fast_op(self, val: str) -> None:
        del self.locals[val]

    def build_string_op(self, cnt: int) -> None:
        self.push("".join(self.popn(cnt)))

    def for_iter_op(self, val: int) -> None:
        top = self.top()

        try:
            mean = top.__next__()
            self.push(mean)
        except StopIteration:
            self.pop()
            self.offset = val

    def binary_and_op(self, _: tp.Any) -> None:
        val1, val2 = self.popn(2)
        self.push(val1 & val2)

    def inplace_and_op(self, _: tp.Any) -> None:
        val1, val2 = self.popn(2)
        self.push(val1 & val2)

    def binary_floor_divide_op(self, _: tp.Any) -> None:
        val1, val2 = self.popn(2)
        self.push(val1 // val2)

    def inplace_floor_divide_op(self, _: tp.Any) -> None:
        val1, val2 = self.popn(2)
        self.push(val1 // val2)

    def inplace_power_op(self, _: tp.Any) -> None:
        val1, val2 = self.popn(2)
        self.push(val1 ** val2)

    def binary_rshift_op(self, _: tp.Any) -> None:
        val1, val2 = self.popn(2)
        self.push(val1 >> val2)

    def inplace_rshift_op(self, _: tp.Any) -> None:
        val1, val2 = self.popn(2)
        self.push(val1 >> val2)

    def binary_lshift_op(self, _: tp.Any) -> None:
        val1, val2 = self.popn(2)
        self.push(val1 << val2)

    def inplace_or_op(self, _: tp.Any) -> None:
        val1, val2 = self.popn(2)
        self.push(val1 | val2)

    def binary_or_op(self, _: tp.Any) -> None:
        val1, val2 = self.popn(2)
        self.push(val1 | val2)

    def binary_subtract_op(self, _: tp.Any) -> None:
        val1, val2 = self.popn(2)
        self.push(val1 - val2)

    def inplace_subtract_op(self, _: tp.Any) -> None:
        val1, val2 = self.popn(2)
        self.push(val1 - val2)

    def binary_true_divide_op(self, _: tp.Any) -> None:
        val1, val2 = self.popn(2)
        self.push(val1 / val2)

    def binary_xor_op(self, _: tp.Any) -> None:
        val1, val2 = self.popn(2)
        self.push(val1 ^ val2)

    def inplace_xor_op(self, _: tp.Any) -> None:
        val1, val2 = self.popn(2)
        self.push(val1 ^ val2)

    def pop_jump_if_true_op(self, val: int) -> None:
        if self.pop():
            self.offset = val

    def pop_jump_if_false_op(self, val: int) -> None:
        if not self.pop():
            self.offset = val

    def jump_forward_op(self, val: int) -> None:
        self.offset = val

    def jump_absolute_op(self, val: int) -> None:
        self.offset = val

    def inplace_lshift_op(self, _: tp.Any) -> None:
        val1, val2 = self.popn(2)
        self.push(val1 << val2)

    def inplace_modulo_op(self, _: tp.Any) -> None:
        val1, val2 = self.popn(2)
        self.push(val1 % val2)

    def unary_positive_op(self, _: tp.Any) -> None:
        self.push(self.pop())


class VirtualMachine:
    def run(self, code_obj: types.CodeType) -> None:
        """
        :param code_obj: code for interpreting
        """
        globals_context: dict[str, tp.Any] = {}
        frame = Frame(code_obj, builtins.globals()['__builtins__'], globals_context, globals_context)
        return frame.run()
