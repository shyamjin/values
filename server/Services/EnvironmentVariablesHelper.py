
def validate_env_vars(env_vars):
    for env_var in env_vars:
        validate_single_env_var(env_var)


def validate_single_env_var(env_var):
    if (env_var.get('name') is None) \
            or (env_var.get('name') == ''):
        raise Exception("Its mandatory to provide a Name for environment variables")

