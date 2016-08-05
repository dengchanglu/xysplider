import sys
import logging
from argparse import ArgumentParser


def main():
    ap = ArgumentParser()
    ap.add_argument('--debug', action='store_true')
    ap.add_argument('--loglevel', default=logging.INFO)
    ap.add_argument('others', nargs='*')
    args = ap.parse_args()

    #logging.basicConfig(level=args.loglevel)

    print >>sys.stderr, 'SYS ARGV', sys.argv
    print 'ARGS', args
    logger = logging.getLogger('test')
    logger.setLevel(args.loglevel)
    logger.error('test logger ERROR level')
    logger.info('test logger INFO level')
    logger.debug('test logger DEBUG level')
    # Root logger
    #logging.root.setLevel(args.loglevel)
    logging.error('root ERROR level')
    logging.info('root INFO level')
    logging.debug('root DEBUG level')

if __name__ == '__main__':
    sys.exit(main())