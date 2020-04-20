import lldb

import subprocess


@lldb.command("pipe")
def pipe_to_shell(
    debugger: lldb.SBDebugger,
    command: str,
    result: lldb.SBCommandReturnObject,
    internal_dict: dict,
):
    i: lldb.SBCommandInterpreter = debugger.GetCommandInterpreter()
    r: lldb.SBCommandReturnObject = lldb.SBCommandReturnObject()

    commands = command.split("|", 1)
    if len(commands) < 2 or len(commands[1]) == 0:
        result.AppendMessage("You need something to pipe to.")
        return

    left = commands[0]
    right = commands[1]

    command_retobj = lldb.SBCommandReturnObject()
    res = i.HandleCommand(left, command_retobj, False)
    out = command_retobj.GetOutput()
    err = command_retobj.GetError()

    if (
        res != lldb.eReturnStatusSuccessFinishResult
        and res != lldb.eReturnStatusSuccessFinishNoResult
    ):
        print(command_retobj.GetError())
        return

    shell_process = subprocess.Popen(right, stdin=subprocess.PIPE, shell=True)
    if out is None or len(out) == 0:
        shell_process.communicate("")
    else:
        shell_process.communicate(out.encode("utf-8"))
    shell_process.wait()


@lldb.command("pudbpipe")
def pudb_pipe_to_shell(
    debugger: lldb.SBDebugger,
    command: str,
    result: lldb.SBCommandReturnObject,
    internal_dict: dict,
):
    import pudb

    pudb.set_trace()
    return pipe_to_shell(debugger, command, result, internal_dict)

