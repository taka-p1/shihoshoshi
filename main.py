from robot import robot
import configparser

def main():
    try:
        conf = configparser.ConfigParser()
        conf.read('config.ini')
        r = robot.Robot(conf['general']['CHROME_DRIVER_PATH'])
        df = r.make_shihoshoshi_df(conf['web']['SHIHOSHOSHI_URL'])
        r.export_file(df, conf['general']['FILE_NAME'])
    finally:
        r.quit_driver()

if __name__ == "__main__":
    main()