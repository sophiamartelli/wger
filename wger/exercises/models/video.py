#  This file is part of wger Workout Manager <https://github.com/wger-project>.
#  Copyright (C) 2013 - 2021 wger Team
#
#  wger Workout Manager is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  wger Workout Manager is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Standard Library
import pathlib
import uuid

# Django
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _


try:
    # Third Party
    import ffmpeg
except ImportError:
    ffmpeg = None

# wger
from wger.exercises.models import ExerciseBase
from wger.utils.models import AbstractLicenseModel


def validate_video(value):

    if value.size > 1024 * 1024 * 100:
        raise ValidationError(_('Maximum file size is 100MB.'))

    if value.file.content_type not in ['video/mp4', 'video/webm', 'video/ogg']:
        raise ValidationError(_('File type is not supported'))

    # If ffmpeg can't read the file, it will raise an exception
    if not hasattr(value.file, 'temporary_file_path'):
        raise ValidationError(_('File type is not supported'))

    # ffmpeg is not installed, skip
    if not ffmpeg:
        return

    try:
        ffmpeg.probe(value.file.temporary_file_path())
    except ffmpeg.Error as e:
        raise ValidationError(_('File is not a valid video'))


def exercise_video_upload_dir(instance, filename):
    """
    Returns the upload target for exercise videos
    """
    ext = pathlib.Path(filename).suffix
    return f"exercise-video/{instance.exercise_base.id}/{instance.uuid}{ext}"


class ExerciseVideo(AbstractLicenseModel, models.Model):
    """
    Model for an exercise image
    """

    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        verbose_name='UUID',
    )
    """Globally unique ID, to identify the image across installations"""

    exercise_base = models.ForeignKey(
        ExerciseBase,
        verbose_name=_('Exercise'),
        on_delete=models.CASCADE,
    )
    """The exercise the image belongs to"""

    is_main = models.BooleanField(
        verbose_name=_('Main video'),
        default=False,
    )
    """A flag indicating whether the video is the exercise's main one"""

    video = models.FileField(
        verbose_name=_('Video'),
        upload_to=exercise_video_upload_dir,
        validators=[validate_video],
    )
    """Uploaded video"""

    size = models.IntegerField(
        verbose_name=_('Size'),
        default=0,
        editable=False,
    )
    """The video filesize, in bytes"""

    duration = models.DecimalField(
        verbose_name=_('Duration'),
        default=0,
        editable=False,
        max_digits=12,
        decimal_places=2,
    )
    """The video duration, in seconds"""

    width = models.IntegerField(
        verbose_name=_('Width'),
        default=0,
        editable=False,
    )
    """The video width, in pixels"""

    height = models.IntegerField(
        verbose_name=_('Height'),
        default=0,
        editable=False,
    )
    """The video height, in pixels"""

    codec = models.CharField(
        verbose_name=_('Codec'),
        max_length=30,
        default='',
        editable=False,
    )
    """The video codec"""

    codec_long = models.CharField(
        verbose_name=_('Codec, long name'),
        max_length=100,
        default='',
        editable=False,
    )
    """The video codec, in full"""

    class Meta:
        """
        Set default ordering
        """
        ordering = ['-is_main', 'id']

    def get_owner_object(self):
        """
        Video has no owner information
        """
        return False

    def save(self, *args, **kwargs):
        """
        Save metadata about the video if ffmpeg is installed
        """
        if ffmpeg and not self.pk and hasattr(self.video.file, 'temporary_file_path'):
            probe_result = ffmpeg.probe(self.video.file.temporary_file_path())
            self.size = probe_result['format']['size']
            self.duration = probe_result['format']['duration']

            # Streams are stored in a list, and we don't know which one is the video stream
            for stream in probe_result['streams']:

                if stream['codec_type'] != 'video':
                    continue

                # Read out video information
                self.width = stream['width']
                self.height = stream['height']
                self.codec = stream['codec_name']
                self.codec_long = stream['codec_long_name']

        super(ExerciseVideo, self).save(*args, **kwargs)
