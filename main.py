from datetime import datetime
import tkinter
import tkinter.messagebox
import customtkinter
from tkinter import filedialog
import tksheet
from PIL import Image, ImageTk

# Appearance Modes: "System", "Dark", "Light"
customtkinter.set_appearance_mode("Light")

# Appearance Themes: "blue", "green", "dark-blue"
customtkinter.set_default_color_theme("blue")

DEFAULT_FONT_SIZE = 15


def calculate_salience(file):
    app.textbox2.delete("0.0", tkinter.END)
    app.textbox3.delete("0.0", tkinter.END)
    # This section initializes all major variables at once and
    # sets them, where necessary, to zero or empty.
    global all_words, words_salience, lines
    all_words, words_salience = {}, {}
    count = 0
    line_number = 0

    # This section opens the file in read-only mode and reads
    # each line one-by-one, stripping the newline at the end
    # of each, and treating each line as the freelist of a
    # different participant.
    input = open(file, "r")
    lines = input.readlines()

    app.textbox2.insert(tkinter.END, ("-" * 100) + "\n")
    app.textbox2.insert(tkinter.END, " ALL RESULTS" + "\n")
    app.textbox2.insert(tkinter.END, ("-" * 100) + "\n")

    for line in lines:
        line = line.strip()

        # This section splits each line (i.e. each freelist) at
        # spaces and checks to see if each word has already been
        # included in the list of all words. If so, then the total
        # frequency increases by one; if not, then it is added to
        # the list and assigned a frequency of one.
        app.textbox3.insert(tkinter.END, ("-" * 100) + "\n")
        app.textbox3.insert(tkinter.END, " PARTICIPANT #" + str(line_number + 1) + "\n")
        app.textbox3.insert(tkinter.END, ("-" * 100) + "\n")

        for word in line.split(" "):
            if word in all_words:
                all_words[word] += 1
            else:
                all_words[word] = 1
            count += 1
            length_of_list = len(line.split(" "))
            word_rank = line.split(" ").index(word)
            ranked_position = length_of_list - word_rank
            salience_in_list = "{:.2f}".format(ranked_position / length_of_list)

            # This section checks to see if the word is already in
            # the dictionary containing the freelist-specific salience
            # of that word. If so, then the salience of the new occurrence
            # is added to the extant value of any previous sums of
            # freelist-specific salience. If not, then the word is added
            # to the list, and the freelist-specific salience is assigned
            # as the value.
            if word in words_salience:
                words_salience[word] += float(salience_in_list)
            else:
                words_salience[word] = float(salience_in_list)

            # This line adds a new row of data to the table, which
            # includes the position in the list, the word itself,
            # the reverse-position in the list, and its salience
            # within that list itself. The position in the list has
            # to be reversed; otherwise, lower-listed items would
            # receive a higher score and, thus, provide wildly
            # inaccurate results.
            app.textbox3.insert(
                tkinter.END,
                "{:<8}{:<8}{:>8}{:>40}".format(
                    count, ranked_position, salience_in_list, word
                ),
            )
            app.textbox3.insert(tkinter.END, "\n")
        app.textbox3.insert(tkinter.END, "\n")

        # This section resets the counter to zero and prints the table
        # and the participant number, which corresponds to the line,
        # i.e. if the data come from the third line, then this would
        # refer to the third participant.
        count = 0
        line_number += 1


def word_frequency(all_words):
    # This section provides the headers and padding for the
    # tables concerning the word frequency (N/%) and overall
    # composite salience. It also calculates the total number
    # of unique words.
    total_word_count = 0

    for frequency in all_words.values():
        total_word_count += frequency

    # This section utilizes the previous list of all words
    # and calculates the composite salience to two decimals
    # by dividing the summed freelist salience of each item
    # by the total number of participants (i.e. lines).
    for word, frequency in all_words.items():
        cognitive_salience = "{:.2f}".format(words_salience[word] / len(lines))
        word_frequency_percentage = "{:.2f}".format(
            (frequency / total_word_count) * 100
        )
        # app.table.insert_row([word, frequency, str(word_frequency_percentage), str(cognitive_salience)])
        app.textbox2.insert(
            tkinter.END,
            "{:<8}{:<8}{:>8}{:>40}".format(
                frequency, word_frequency_percentage, cognitive_salience, word
            ),
        )
        app.textbox2.insert(tkinter.END, "\n")
    app.textbox2.insert(tkinter.END, "\n")

    # This section prints two different tables. Both contain
    # the word, its frequency of occurrence, and its composite
    # salience. The difference, however, is that the first
    # table sorts it by frequency; the second, by salience.


def open_file():
    global filename
    filename = filedialog.askopenfilename()
    if filename:
        print("Opening file...", end="")
        with open(filename, "r") as file:
            try:
                content = file.read()
                content = content.strip()
                app.textbox1.delete("0.0", tkinter.END)
                app.textbox1.insert("0.0", content)
                print("done")
            except:
                print("error encountered")

        # clear existing text and print imported file to textbox
        app.entry.delete(0, tkinter.END)
        app.entry.insert(0, filename)


def analyze():
    try:
        print("Analyzing file...", end="")
        if filename:
            calculate_salience(filename)
            word_frequency(all_words)
            print("done")
        else:
            print("error encountered.")
    except:
        print("no file imported.")


def clear():
    try:
        print("Clearing data...", end="")
        app.entry.delete(0, tkinter.END)
        app.textbox1.delete("0.0", tkinter.END)
        app.textbox2.delete("0.0", tkinter.END)
        app.textbox3.delete("0.0", tkinter.END)
        app.textbox2.insert(
            "0.0",
            "### Please type or import data first, and then click on the 'Analyze' button to populate this tab. ###",
        )
        app.textbox3.insert(
            "0.0",
            "### Please type or import data first, and then click on the 'Analyze' button to populate this tab. ###",
        )
        filename = ""
        print("done")
    except:
        print("Error clearing data.")


def write_to_log(message):
    with open("log.txt", "a") as logfile:
        try:
            logfile.write(message + "\n")
        except:
            print("Error writing to log file.")


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        print("Building window...", end="")
        self.title("PyAnthropac")
        self.geometry(f"{1100}x{580}")
        print("done")

        # configure grid layout (4x4)
        print("Building grids...", end="")
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)
        print("done")

        print("Adding widgets...", end="")
        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=5, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(
            self.sidebar_frame,
            text="PyAnthropac",
            font=customtkinter.CTkFont(family="Consolas", size=25, weight="bold"),
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        import_image = customtkinter.CTkImage(
            Image.open("assets/import.png"), size=(26, 26)
        )
        self.sidebar_button_1 = customtkinter.CTkButton(
            self.sidebar_frame,
            text="Import Data",
            anchor="w",
            command=open_file,
            font=customtkinter.CTkFont(size=DEFAULT_FONT_SIZE, weight="bold"),
            image=import_image,
        )
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")

        analyze_image = customtkinter.CTkImage(
            Image.open("assets/analyze.png"), size=(26, 26)
        )
        self.sidebar_button_2 = customtkinter.CTkButton(
            self.sidebar_frame,
            text="Analyze Salience",
            anchor="w",
            command=analyze,
            font=customtkinter.CTkFont(size=DEFAULT_FONT_SIZE, weight="bold"),
            image=analyze_image,
        )
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")

        clear_image = customtkinter.CTkImage(
            Image.open("assets/clear.png"), size=(26, 26)
        )
        self.sidebar_button_4 = customtkinter.CTkButton(
            self.sidebar_frame,
            text="Clear All",
            anchor="w",
            command=clear,
            font=customtkinter.CTkFont(size=DEFAULT_FONT_SIZE, weight="bold"),
            image=clear_image,
        )
        self.sidebar_button_4.grid(row=3, column=0, padx=20, pady=10, sticky="nsew")

        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(
            self.sidebar_frame,
            values=["Select Theme", "Light", "Dark"],
            command=self.change_appearance_mode_event,
        )
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))

        # create main entry and button
        self.entry = customtkinter.CTkEntry(self)
        self.entry.grid(
            row=3, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew"
        )
        print("done")

        # create tabview
        print("Building tabviews...", end="")
        self.tabview = customtkinter.CTkTabview(self, width=250)
        self.tabview.grid(
            row=0,
            column=1,
            columnspan=3,
            rowspan=3,
            padx=(20, 0),
            pady=(20, 0),
            sticky="nsew",
        )
        self.tabview.add("Raw Data")
        self.tabview.add("Data Overview")
        self.tabview.add("Individual Results")
        self.tabview.add("How to Use")
        print("done")

        # create textbox
        print("Building raw data notebook...", end="")
        self.textbox1 = customtkinter.CTkTextbox(
            self.tabview.tab("Raw Data"),
            font=customtkinter.CTkFont(size=DEFAULT_FONT_SIZE),
        )
        self.textbox1.grid(
            row=0,
            column=0,
            columnspan=3,
            rowspan=3,
            padx=(20, 0),
            pady=(20, 0),
            sticky="nsew",
        )
        self.textbox1.pack(fill="both", expand=True)
        print("done")

        # create textbox
        print("Building help notebook...", end="")
        self.textbox4 = customtkinter.CTkTextbox(
            self.tabview.tab("How to Use"),
            font=customtkinter.CTkFont(size=DEFAULT_FONT_SIZE),
        )
        self.textbox4.grid(
            row=0,
            column=0,
            columnspan=3,
            rowspan=3,
            padx=(20, 0),
            pady=(20, 0),
            sticky="nsew",
        )
        self.textbox4.pack(fill="both", expand=True)
        print("done")

        # create textbox
        print("Building data overview notebook...", end="")
        self.textbox2 = customtkinter.CTkTextbox(self.tabview.tab("Data Overview"))
        self.textbox2.grid(
            row=0,
            column=0,
            columnspan=3,
            rowspan=3,
            padx=(20, 0),
            pady=(20, 0),
            sticky="nsew",
        )
        self.textbox2.pack(fill="both", expand=True)
        print("done")

        # individual results
        print("Building individual results notebook...", end="")
        self.textbox3 = customtkinter.CTkTextbox(self.tabview.tab("Individual Results"))
        self.textbox3.grid(
            row=0,
            column=0,
            columnspan=3,
            rowspan=3,
            padx=(20, 0),
            pady=(20, 0),
            sticky="nsew",
        )
        self.textbox3.pack(fill="both", expand=True)
        print("done")

        print("Inserting default values...", end="")
        # set default values
        self.textbox3.insert(
            "0.0",
            "### Please import data first, and then click on the 'Analyze' button to populate this tab. ###",
        )
        self.textbox4.insert(
            "0.0",
            """----------------------------------------------------------------------------------------------------\n PyAnthropac v0.1\n Created by Troy E. Spier, Ph.D.\n----------------------------------------------------------------------------------------------------\n\nQ: How can I import my data?\n\nA: You can import your data from a file on the left side of this program. Once you have done that, you should see the filepath listed in the input box below. Next, click on the 'Analyze'\n     button to calculate the results.\n\nQ: How should my data be formatted?\n\nA: One line corresponds to one respondent, and one space corresponds to a different response from that respondent. If any of the responses normally contain a space, they must\n     consistently be 'joined' with some other form of punctuation, such as a hyphen or underscore; otherwise, these will be treated as different responses.\n\nQ: How are the calculations performed?\n\nA: The composite salience for responses is determined by first identifying how many respondents there are and then by splitting each respondent's responses at the delimiter selected\n     by you. Next, two concurrent sets of data are computed. The first includes the respondent-specific information, including the ranked points per response and the salience of that item\n     within the individual list. Second, the frequency and the position in each list relative to the length of the list are considered in identifying the composite salience. In mathematical terms,\n     the formula used comes from Sutrop (2001): S = F2 /(N Σ R j)\n\nQ: What is freelisting?\n\nA: Freelisting rests on three fundamental assumptions. First, participants will list items in the order of familiarity, i.e. if they are more familiar with a particular item, then this item will\n     appear before other lesser-known or less familiar items. Second, participants who are more familiar than other participants with a particular domain will list more numerous and specific\n     items than others. Third, participants will generally begin with items that are more common in their own spatiotemporal environments.\n\nQ: What is cognitive salience?\n\nA: Salience refers to the understanding that certain items are perceptually more important, significant, relevant, etc. than others. For instance, if a word occurs more frequently than others\n     in a text (e.g. 'depressed' instead of 'angry'), then we would suggest that the text's most salient tone is one of sadness. Similarly, salience in freelisting considers both the frequency of\n     identification and the position within the list. For example, an item that occurs more often than others and in a more immediate position suggests greater salience, i.e. resulting in a\n     distinction among word frequency, freelist salience, cognitive salience, and psychological salience.\n\nQ: Why would I want to use this?\n\nA: Well, it could give you some insight into the cultural knowledge within a particular domain among your respondents. For instance, I was able to replicate similar results to Eleanor\n     Rosch's study on birdiness. Similarly, I was able to gauge how my students defined musical and cinematic genres based on their exposure. Other scholars, including those listed below,\n     have done (perhaps) more interesting things. You can, too!\n\n----------------------------------------------------------------------------------------------------\n Relevant Academic Scholarship:\n----------------------------------------------------------------------------------------------------\n\nBolton, Curtis R. et al. 1980. "Nepali Color Terms: Salience in a Listing Task." Journal of the Steward Anthropological Society, 12: 309-21.\n\nBorgatti, Stephen P. 1990. "Using Anthropac to Investigate a Cultural Domain." Cultural Anthropology Methods Newsletter, 2(1): 8.\n\n---. 1999. Elicitation Techniques for Cultural Domain Analysis. In: Schensul J, LeCompte M, editors. The Ethnographer's Toolkit. Walnut Creek: AltaMira Press, pp. 115-51.\n\nKeddem, Shimrit et al. 2021. \"Practical Guidance for Studies Using Freelisting Interviews.\" Preventing Chronic Disease: Public Health Research, Practice, and Policy 18(4): 1-8.\n\nQuinlan, Marsha B. 2017. \"The Freelisting Method.\" Handbook of Research Methods in Health Social Sciences. 1431-1446.\n\nSchrauf, Robert W. and Julia Sanchez. 2008.  \"Using Freelisting to Identify, Assess, and Characterize Age Differences in Shared Cultural Domains.\" The Journals of Gerontology:\n     Series B, 63(6): S385-S393.\n\nSmith, Jerome. 1993. \"Using ANTHROPAC 3.5 and a Spreadsheet to Compute a Free-List Salience Index.\" Field Methods 5(3): 1-3.\n\nSmith, Jerome et al. 1995. \"Salience Counts: A Domain Analysis of English Color Terms.\" Journal of Linguistic Anthropology 5(2): 203-216.\n\nSmith, Jerome and Stephen P. Borgatti. 1998. \"Salience Counts--And So Does Accuracy: Correcting and Updating a Measure for Free-List-Item Salience.\" Journal of Linguistic\n     Anthropology 7(2): 208-209.\n\nSutrop, Urmas. 2001. "List Task and a Cognitive Salience Index." Field Methods, 13(3): 263-276.""",
        )
        print("done")
        print("Program initialized successfully.")

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)


if __name__ == "__main__":
    app = App()
    customtkinter.CTkFont(size=15)
    app.attributes("-zoomed", "True")
    app.mainloop()
