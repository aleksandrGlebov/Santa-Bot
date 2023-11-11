from functools import wraps

def validate_text_input(state_if_error):
    def decorator_wrapper(func):
        @wraps(func)
        def wrapped(update, context):
            text_input = update.message.text
            
            if not text_input:
                update.message.reply_text("Пожалуйста, введите корректные данные.")
                return state_if_error
            
            if  len(text_input) > 256:
                update.message.reply_text("Введенный текст слишком длинный. Пожалуйста, сократите его.")
                return state_if_error
            
            if  len(text_input) < 3:
                update.message.reply_text("Введенный текст слишком короткий.")
                return state_if_error

            if not any(char.isalpha() for char in text_input):
                update.message.reply_text("Введенный текст должен содержать хотя бы одну букву.")
                return state_if_error

            return func(update, context)

        return wrapped
    return decorator_wrapper

def validate_numeric_input(min_value, max_value, error_state, float_allowed=True):
    def decorator_wrapper(func):
        @wraps(func)
        def wrapped(update, context):
            value = update.message.text

            if not value.replace('.', '', 1).isdigit() or (float_allowed and '.' in value and value.count('.') > 1):
                update.message.reply_text("Пожалуйста, введите число.")
                return error_state
            
            numeric_value = float(value) if float_allowed and '.' in value else int(value)

            if not (min_value <= numeric_value <= max_value):
                update.message.reply_text(f"Пожалуйста, введите число в диапазоне от {min_value} до {max_value}.")
                return error_state
            
            context.user_data['validated_value'] = numeric_value
            return func(update, context)
        
        return wrapped
    return decorator_wrapper