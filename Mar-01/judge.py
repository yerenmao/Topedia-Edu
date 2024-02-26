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
        try:
            result = subprocess.run([sys.executable, ans_file], input=input_data, text=True, capture_output=True, timeout=5)
            if result.returncode:
                Color.print('Runtime Error (RE)', fg=Color.fg.red); idx += 1; continue

            user_output_data = result.stdout.strip()
            correct_output_data, user_output_data = correct_output_data.split('\n'), user_output_data.split('\n')
            if len(correct_output_data) != len(user_output_data):
                Color.print('Wrong Answer (WA)', fg=Color.fg.red)
            else:
                is_AC, is_WA = True, False
                for correct_line, user_line in zip(correct_output_data, user_output_data):
                    if correct_line != user_line:
                        is_AC = False
                        if correct_line.strip() != user_line.strip():
                            is_WA = True; break
                if is_AC: Color.print('Accepted (AC)', fg=Color.fg.white)
                elif is_WA: Color.print('Wrong Answer (WA)', fg=Color.fg.red)
                else: Color.print('Presentation Error (PE)', fg=Color.fg.red)

        except subprocess.TimeoutExpired:
            Color.print('Time Limit Exceeded (TLE)', fg=Color.fg.red)
        except Exception as e:
            Color.print('Runtime Error (RE)', fg=Color.fg.red)
            Color.print('Error: ', e, fg=Color.fg.red)
        idx += 1


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

