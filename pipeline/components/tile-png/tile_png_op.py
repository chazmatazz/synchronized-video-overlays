#!/usr/bin/env python3

import sys
import op
import op_helper

def getArgs(fn, inputs):
    return [a for lst in list(map(list, zip(inputs[::2], fn(inputs[1::2])))) for a in lst]

class TilePngOp(op.Op):
    def get_in_args(self):
        return getArgs(op_helper.create_in_args, self.args.input_uris)

if __name__ == '__main__':
    args = sys.argv[1:]
    print("Op args", args)
    #print(getArgs(lambda lst: [f'foo{x}' for x in lst], args))
    opp = TilePngOp(op.parse_arguments(args))
    opp.run()
