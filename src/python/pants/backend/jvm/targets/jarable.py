# Copyright 2014 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).

from abc import ABC, abstractmethod

from pants.java.jar.jar_dependency import JarDependency


class Jarable(ABC):
    """A mixin that identifies a target as one that can provide a jar.

    :API: public
    """

    @property
    @abstractmethod
    def identifier(self):
        """Subclasses should return a stable unique identifier for the jarable target."""

    @property
    def provides(self):
        """Returns an optional :class:`pants.backend.jvm.targets.artifact.Artifact` if this target
        is exportable.

        Subclasses should override to provide an artifact descriptor when one applies, by default
        None is supplied.
        """
        return None

    def get_artifact_info(self):
        """Returns a tuple composed of a :class:`pants.java.jar.JarDependency` describing the jar
        for this target and a bool indicating if this target is exportable."""
        exported = bool(self.provides)

        org = self.provides.org if exported else "internal"
        name = self.provides.name if exported else self.identifier

        # TODO(John Sirois): This should return something less than a JarDependency encapsulating just
        # the org and name.  Perhaps a JarFamily?
        return JarDependency(org=org, name=name, rev=None), exported
