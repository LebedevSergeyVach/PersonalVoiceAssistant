#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <libgen.h>

int main(int argc, char *argv[]) {
    const char *python_interpreter = "python";

    const char *script_path = "src\\main.py";

    char *executable_path = strdup(argv[0]);

    char *dir_path = dirname(executable_path);

    char full_script_path[1024];
    snprintf(full_script_path, sizeof(full_script_path), "%s\\%s", dir_path, script_path);

    for (int i = 0; full_script_path[i]; i++) {
        if (full_script_path[i] == '\\') {
            full_script_path[i] = '/';
        }
    }

    char command[2048];
    snprintf(command, sizeof(command), "%s %s", python_interpreter, full_script_path);

    printf("Running voice assistent");

    int result = system(command);

    if (result != 0) {
        fprintf(stderr, "Failed to run command: %s\n", command);
        return 1;
    }

    free(executable_path);

    return 0;
}
