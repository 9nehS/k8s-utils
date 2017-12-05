#!/usr/bin/env python
import argparse
import logging
import os
import sys

DEFAULT_LOG_LEVEL = logging.INFO
# DEFAULT_LOG_FORMAT = '%(asctime)s-%(levelname)s-%(name)s-%(filename)s:%(lineno)s - %(message)s'
DEFAULT_LOG_FORMAT = '%(asctime)s[%(levelname)s][%(name)s][%(filename)s]:%(lineno)s - %(message)s'

CLOUD_K8S_PATH = '/opt/mrkcloud/cloud-ops/k8s/cloud/'
API_K8S_PATH = ''

ENVSUB_SHELL = 'envsubst.sh'
API_ENV_SHELL = 'market/szhao-k8s.sh'
METEOR_ENV_SHELL = 'szhao-k8s.sh'
API_YAML = 'market/marketing_debug.yaml'
METEOR_YAML = 'yaml/cloud-meteor.yaml'

KUBECTL_APPLY_CMD = 'kubectl apply -f -'
FULL_KUBECTL_APPLY_CMD = None


def get_logger(logger_name, logger_level=DEFAULT_LOG_LEVEL, logger_stream=sys.stdout):
    logger = logging.getLogger(logger_name)
    logging.basicConfig(format=DEFAULT_LOG_FORMAT, stream=logger_stream)
    logger.setLevel(logger_level or DEFAULT_LOG_LEVEL)
    return logger


def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--component', dest='component', help='Component to be updated, e.g. meteor|api',
                        required=True)
    parser.add_argument('-i', '--image-version', dest='img_ver', help='Image versions to be deployed, e.g. 2017.12.1',
                        required=True)
    args = parser.parse_args()
    return args


def main():
    logger = get_logger('CMC_deploy_update')
    args = get_parser()
    if args.component.lower() == 'api':
        FULL_KUBECTL_APPLY_CMD = 'IMAGE_VERSION=' + args.img_ver + ' ' + 'MODE=meteor' + ' ' \
                                 + './' + ENVSUB_SHELL + ' -e ' + API_ENV_SHELL + ' ' + API_YAML + ' | ' \
                                 + KUBECTL_APPLY_CMD
        logger.info('CMD for API update: %s' % FULL_KUBECTL_APPLY_CMD)
        logger.info('Will apply the new API deployment')
        os.system('cd' + ' ' + CLOUD_K8S_PATH + ';' + FULL_KUBECTL_APPLY_CMD)
        logger.info('New API deployment completed')
    elif args.component.lower() == 'meteor':
        FULL_KUBECTL_APPLY_CMD = 'IMAGE_VERSION=' + args.img_ver + ' ' + '../' + ENVSUB_SHELL + ' -e ' \
                                 + METEOR_ENV_SHELL + ' ' + METEOR_YAML + ' | ' + KUBECTL_APPLY_CMD
        logger.info('CMD for meteor update: %s' % FULL_KUBECTL_APPLY_CMD)
        logger.info('Will apply the new meteor deployment')
        os.system('cd' + ' ' + CLOUD_K8S_PATH + 'meteor;' + FULL_KUBECTL_APPLY_CMD)
        logger.info('New meteor deployment completed')


if __name__ == '__main__':
    main()
