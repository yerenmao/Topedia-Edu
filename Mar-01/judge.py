import os
import sys
import shutil
import subprocess

from colorutil import Color


def judge(ans_file: str, num: int):

    # intro
    intro = f' problem: {num}, your file: {ans_file} '
    print(f'+-{"-"*len(intro)}-+')
    print(f'| {intro} |')
    print(f'+-{"-"*len(intro)}-+')
    
    # list testcase/p{num}
    inputfile_list = sorted([i for i in os.listdir(f'testcase/p{num}/') if 'input' in i])
    outputfile_list = sorted([i for i in os.listdir(f'testcase/p{num}/') if 'output' in i])
    if len(inputfile_list) != len(outputfile_list):
        Color.print(f'Judge: number of I/O does not match', fg=Color.fg.lightred)
        return

    failed_testcase = []
    # judge each pair of IO
    idx = 1
    for inputfile, outputfile in zip(inputfile_list, outputfile_list):
        # read input data
        with open(f'testcase/p{num}/{inputfile}') as infile:
            input_data = infile.read().strip()
        with open(f'testcase/p{num}/{outputfile}') as outfile:
            correct_output_data = outfile.read().strip()

        # print testcase
        Color.print(f'* testcase {idx} - ', fg=Color.fg.yellow, end='', flush=True)
        # judging
        judge_result = 'AC'
        try:
            result = subprocess.run([sys.executable, ans_file], input=input_data, text=True, capture_output=True, timeout=5)
            if result.returncode:
                judge_result = 'RE'
        except subprocess.TimeoutExpired:
            judge_result = 'TLE'
        except Exception as e:
            Color.print('Error: ', e, fg=Color.fg.red);
            failed_testcase.append(idx); idx += 1; continue

        # diff
        if judge_result == 'AC':
            user_output_data = result.stdout.strip()
            correct_output_data, user_output_data = correct_output_data.split('\n'), user_output_data.split('\n')
            if len(correct_output_data) != len(user_output_data):
                judge_result = 'WA'
            else:
                for correct_line, user_line in zip(correct_output_data, user_output_data):
                    if correct_line != user_line:
                        if correct_line.strip() != user_line.strip():
                            judge_result = 'WA'; break
                        judge_result = 'PE'

        if judge_result == 'AC':
            Color.print('Accepted (AC)', fg=Color.fg.green)
        else:
            failed_testcase.append(idx)
            match judge_result:
                case 'RE': Color.print('Runtime Error (RE)', fg=Color.fg.red)
                case 'TLE': Color.print('Time Limit Exceeded (TLE)', fg=Color.fg.red)
                case 'WA': Color.print('Wrong Answer (WA)', fg=Color.fg.red)
                case 'PE': Color.print('Presentation Error (PE)', fg=Color.fg.red)
        idx += 1

    # print result
    if len(failed_testcase) == 0:
        final_result = f'All {idx-1} testcase passed'
    else:
        final_result = f'testcase {str(failed_testcase).strip("[]")} failed'
    print(f'+-{"-"*len(final_result)}-+')
    print('| ', end=''); Color.print(final_result, fg=(Color.fg.green if len(failed_testcase) == 0 else Color.fg.red), end=''); print(' |')
    print(f'+-{"-"*len(final_result)}-+')


if __name__ == '__main__':
    # check user input
    if len(sys.argv) != 3:
        Color.print('Usage: python3 judge.py ans.py problem_number', fg=Color.fg.yellow)
        sys.exit(1)

    ans_file = sys.argv[1]
    if not sys.argv[2].isnumeric():
        Color.print(f'Judge: "{sys.argv[2]}" is not a problem_number', fg=Color.fg.lightred)
        sys.exit(1)
    num = int(sys.argv[2])

    if f'p{num}' not in os.listdir('testcase'):
        Color.print(f'Judge: problem {num} not exist', fg=Color.fg.lightred)
        sys.exit(1)

    # check environment
    if sys.executable in ["", None]:
        Color.print('Judge: sys.executable error', fg=Color.fg.lightred)
        sys.exit(1)

    # Judge
    judge(ans_file, num)

