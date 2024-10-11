import subprocess
import sys
import io

def validate_code(code):
    # Write the code to a temporary file
    with open("temp_code.py", "w") as f:
        f.write(code)
    
    # Redirect stdout and stderr
    old_stdout, old_stderr = sys.stdout, sys.stderr
    redirected_output = sys.stdout = io.StringIO()
    redirected_error = sys.stderr = io.StringIO()
    
    try:
        # Execute the code
        exec(open("temp_code.py").read())
        execution_output = redirected_output.getvalue()
        execution_error = redirected_error.getvalue()
        
        if execution_error:
            return False, execution_error
        return True, execution_output
    except Exception as e:
        return False, str(e)
    finally:
        # Restore stdout and stderr
        sys.stdout, sys.stderr = old_stdout, old_stderr