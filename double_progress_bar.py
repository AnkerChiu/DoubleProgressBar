from PySide6.QtWidgets import QProgressBar, QApplication, QWidget, QVBoxLayout
from PySide6.QtGui import QPainter, QColor
from PySide6.QtCore import QRect, Qt, QTimer

class DoubleColorProgressBar(QProgressBar):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._value1 = 0
        self._animation_value = 0
        self._animation_bar_width = 0
        self._animation_step = 0
        self._format = ""

        # Timer management: centralized start/stop of animation timer
        self._animation_timer = QTimer(self)
        self._animation_timer.timeout.connect(self._update_animation)

    # Helper: calculate ratio for value1 progress within the range
    def _calc_ratio(self):
        min_val = self.minimum()
        max_val = self.maximum()
        if max_val != min_val:
            return (self._value1 - min_val) / (max_val - min_val)
        return 0

    # Helper: calculate bar1 region based on a given value
    def _get_bar1_region(self, value):
        w, h = self.width(), self.height()
        min_val = self.minimum()
        max_val = self.maximum()
        if max_val != min_val:
            ratio = (value - min_val) / (max_val - min_val)
        else:
            ratio = 0
        return QRect(0, 0, int(w * ratio), h)

    @property
    def value1(self):
        return self._value1

    @value1.setter
    def value1(self, v):
        min_val = self.minimum()
        max_val = self.maximum()
        w, h = self.width(), self.height()
        # Compute old bar1 region via helper
        old_rect = self._get_bar1_region(self._value1)
        # Update value1 with bounds checking
        self._value1 = min(max(v, min_val), max_val)
        # Compute new bar1 region via helper
        new_rect = self._get_bar1_region(self._value1)
        update_region = old_rect.united(new_rect)
        self.update(update_region)

    @property
    def value2(self):
        return self._animation_value

    @value2.setter
    def value2(self, v):
        min_val = self.minimum()
        max_val = self.maximum()
        # Add range checking for the animation value
        self._animation_value = min(max(v, min_val), max_val)

    @property
    def format(self):
        return self._format
    
    @format.setter
    def format(self, text):
        self._format = text

    def _start_animation_timer(self, interval):
        self._animation_timer.start(interval)

    def _stop_animation_timer(self):
        self._animation_timer.stop()

    def startAnimation(self, interval=30):
        """Start the animation timer."""
        self._start_animation_timer(interval)

    def stopAnimation(self):
        """Stop the animation timer."""
        self._stop_animation_timer()

    # Helper: compute animation (bar2) region given a value
    def _get_animation_region(self, value):
        w = self.width()
        max_val = self.maximum()
        # Calculate x based on provided value; avoid division by 0
        x = int(w * value / max_val) if max_val > 0 else 0
        return QRect(x, 0, self._animation_bar_width, self.height())

    def _update_animation(self):
        """Update animation's value and redraw the updated region."""
        max_val = self.maximum()

        # Calculate the old region for animation bar
        old_rect = self._get_animation_region(self._animation_value)

        # Animation update logic: increase until reaching value1, then reset
        if self._animation_value + self._animation_step < self._value1:
            self._animation_value += self._animation_step
        else:
            self._animation_value = 0

        # Calculate the new region for animation bar
        new_rect = self._get_animation_region(self._animation_value)
        update_region = old_rect.united(new_rect)
        self.update(update_region)

    def paintEvent(self, event):
        painter = QPainter(self)
        # Limit painting to the region that needs to be updated
        painter.setClipRegion(event.region())
        self._draw_background(painter)
        self._draw_bar1(painter)
        self._draw_animation_bar(painter)
        self._draw_text(painter)

    def _draw_background(self, painter):
        painter.setBrush(QColor("#FFFFFF"))
        painter.setPen(Qt.NoPen)
        painter.drawRect(self.rect())

    def _draw_bar1(self, painter):
        rect_ = self.rect()
        w, h = rect_.width(), rect_.height()
        ratio = self._calc_ratio()
        completed_rect = QRect(rect_.x(), rect_.y(), int(w * ratio), h)
        painter.setBrush(QColor('#40E0D0'))
        painter.drawRect(completed_rect)

    def _draw_animation_bar(self, painter):
        rect_ = self.rect()
        w, h = rect_.width(), rect_.height()
        max_val = self.maximum()
        # Avoid division by 0 for calculating x
        bar_x = int(w * self._animation_value / max_val) if max_val > 0 else 0
        animation_rect = QRect(bar_x, rect_.y(), self._animation_bar_width, h)
        painter.setBrush(QColor('#E0FFFF'))
        painter.drawRect(animation_rect)
    
    def _draw_text(self, painter):
        """Draw the text on the progress bar with template replacement."""
        painter.setPen(QColor("#000000"))
        min_val = self.minimum()
        max_val = self.maximum()
        ratio = self._calc_ratio()
        percentage = int(ratio * 100)
        # Replace placeholders in the format string:
        # %p will be replaced with the percentage
        # %v will be replaced with the current value1
        text = self._format.replace("%p", str(percentage)).replace("%v", str(self._value1))
        painter.drawText(self.rect(), Qt.AlignCenter, text)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._update_animation_dimensions()

    def _update_animation_dimensions(self):
        """Update animation bar's width and step, called when widget size or range changes."""
        w = self.width()
        # For example: set animation bar width to 5% of the total width
        self._animation_bar_width = int(w / 20)
        max_val = self.maximum()
        min_val = self.minimum()
        self._animation_step = 0.05 * (max_val - min_val)

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = QWidget()
    layout = QVBoxLayout(window)

    progress_bar = DoubleColorProgressBar()
    progress_bar.setRange(0, 500)
    progress_bar.value1 = 300
    progress_bar.format = "Hello World... %p% (%v)"
    progress_bar.startAnimation(interval=100)

    layout.addWidget(progress_bar)
    window.setLayout(layout)
    window.show()
    sys.exit(app.exec())