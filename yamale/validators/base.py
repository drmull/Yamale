class BaseValidator(object):
    """Base class for all Validators"""
    constraints = []
    value_type = None

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

        # Is field required? Default is True
        self.is_required = bool(kwargs.pop('required', True))

        # Can value be None if field is optional? Default is True
        self._value_can_be_none = bool(kwargs.pop('none', True))

        # Construct all constraints
        self._constraints_inst = self._create_constraints(self.constraints,
                                                          self.value_type,
                                                          kwargs)

    def _create_constraints(self, constraint_classes, value_type, kwargs):
        constraints = []
        for constraint in constraint_classes:
            constraints.append(constraint(value_type, kwargs))
        return constraints

    @property
    def tag(self):
        return self.__class__

    @property
    def is_optional(self):
        """ used for test """
        return not self.is_required

    def get_name(self):
        return self.tag

    def validate(self, value, schema, path, strict):
        """
        Check if ``value`` is valid.

        :returns: [errors] If ``value`` is invalid, otherwise [].
        """

        # Optional field with optional value? Who cares.
        if (value is None and
                not self.is_required and
                self._value_can_be_none):
            return []

        errors = self._validate(value, schema, path, strict)
        if errors:
            return errors

        # Then validate all the constraints second.
        for constraint in self._constraints_inst:
            error = constraint.is_valid(value, schema, path, strict)
            if error:
                if isinstance(error, list):
                    errors.extend(error)
                else:
                    errors.append(error)

        return errors

    def _validate(self, value, schema, path, strict):
        raise NotImplementedError('You need to override this function')

    def fail(self, value):
        """Override to define a custom fail message"""
        return '\'%s\' is not a %s.' % (value, self.get_name())

    def __repr__(self):
        return '%s(%s, %s)' % (self.__class__.__name__, self.args, self.kwargs)

    def __eq__(self, other):
        # Validators are equal if they have the same args and kwargs.
        eq = [isinstance(other, self.__class__),
              self.args == other.args,
              self.kwargs == other.kwargs]
        return all(eq)


class Validator(BaseValidator):

    def _validate(self, value, schema, path, strict):
        if not self._is_valid(value):
            return [self.fail(value)]
        return []

    def _is_valid(self, value):
        """Validators must implement this. Return True if value is valid."""
        raise NotImplementedError('You need to override this function')

    def is_valid(self, value):
        """Used for test"""
        return self.validate(value, None, None, None) == []
