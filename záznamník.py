import logging
logging.basicConfig(filename='report.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')

try:

    import SRC.main as control

    def main():
        controller = control.main()
        controller.run()


    if __name__ == "__main__":
        main()

except Exception as e:
    logging.exception("caught at main")
    raise e  # personal choice, still want to see error in IDE
