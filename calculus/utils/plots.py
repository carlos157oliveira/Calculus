import matplotlib.pyplot as plt
import numpy as np
import io
# from matplotlib import rcParams

class Plots:

    def n_subplots(title, ranges, functions, labels, colors):
        x = np.linspace(ranges[0], ranges[1], 1000)
        fig, axs = plt.subplots(len(functions))
        fig.suptitle(title)

        for i, f in enumerate(functions):

            try:
                axs[i].plot(x, f(x), color=colors[i], label=labels[i])
            except TypeError:
                # If the lambda function 'f' presents something in the inner
                # logic that doesn't directly support numpy arrays,
                # calculate 'f' for every value before turning into numpy array.
                f_values = np.array([f(i) for i in x])
                axs[i].plot(x, f_values, color=colors[i], label=labels[i])


        fig.legend()
        fig.show()

    def get_buffer_with_text(txt, color):
        # dependency on LaTeX wasn't successfully configured
        # rcParams['text.usetex'] = True

        # old fixed size
        #plt.figure(figsize=(4,0.75))

        # make sure no image is in matplotlib's buffer
        plt.close()

        # Take figure's dpi and calculate size in inches through text size in pixels
        fig = plt.figure()
        dpi = fig.dpi
        r = fig.canvas.get_renderer()
        plt.axis('off')

        textimage = plt.text(
            0.5,
            0.5,
            txt,
            fontsize=20,
            horizontalalignment='center',
            verticalalignment='center',
            color=color)

        bb = textimage.get_window_extent(renderer=r)

        # We multiply by a correction factor of 1.025 to have a little margin
        # Experience showed width is cropped the larger it is without the factor
        width_inches = bb.width * 1.025 / dpi
        height_inches = bb.height * 1.025 / dpi
        fig.set_size_inches(width_inches, height_inches)

        buff = io.BytesIO()

        plt.savefig(buff, format='png', transparent=True)
        return buff


    def open_result_in_external_viewer(txt):
        # make sure no image is in matplotlib's buffer
        plt.close()

        fig = plt.figure()
        plt.axis('off')

        textimage = plt.text(
            0.5,
            0.5,
            txt,
            fontsize=20,
            horizontalalignment='center',
            verticalalignment='center')

        plt.show()

    def save_file_with_result(txt, filename):

        # dependency on LaTeX wasn't successfully configured
        # rcParams['text.usetex'] = True

        # old fixed size
        #plt.figure(figsize=(4,0.75))

        # make sure no image is in matplotlib's buffer
        plt.close()

        # Take figure's dpi and calculate size in inches through text size in pixels
        fig = plt.figure()
        dpi = fig.dpi
        r = fig.canvas.get_renderer()
        plt.axis('off')

        textimage = plt.text(
            0.5,
            0.5,
            txt,
            fontsize=30,
            horizontalalignment='center',
            verticalalignment='center')

        bb = textimage.get_window_extent(renderer=r)

        # We multiply by a correction factor of 1.025 to have a little margin
        # Experience showed width is cropped the larger it is without the factor
        width_inches = bb.width * 1.025 / dpi
        height_inches = bb.height * 1.025 / dpi
        fig.set_size_inches(width_inches, height_inches)

        plt.savefig(filename, format='png')
