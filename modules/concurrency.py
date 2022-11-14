import threading, subprocess, logging as logger
def launch_process_and_stream_log(command):
    def init_logging_process(process):
        while True:
            # Retrieve stdout and stderr line by line from subprocess
            stdout = process.stdout.readline()
            stderr = process.stderr.readline()
            if process.returncode is not None:
                # Break logging loop when subprocess completes
                break
            if stdout:
                logger.info(stdout)
                #stream_the_log_to_somewhere_else_like_kibana(stdout, 'INFO')
            if stderr:
                logger.error(stderr)
                #stream_the_log_to_somewhere_else_like_kibana(stderr, 'ERROR')

    logger.info('Before running process')
    process = subprocess.Popen(
        [command], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    logger.info('Start logging thread process')
    t = threading.Thread(target=init_logging_process, args=(process))  # type: ignore
    t.setDaemon(True)
    t.start()
