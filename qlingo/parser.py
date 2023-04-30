line_number = 0
line_list = []
spaces = 0
tabs = ''

class Parse():
    def __init__(self, filename) -> None:
        self.filename = filename
        f = open(self.filename, 'r+')
        self.reader = f.readlines()
        self.new_con = []
        self.line_index = 0
        for con in self.reader:
            self.line_index += 1
            if self.is_class(con):
                if "Window" not in con:
                    self.new_con.append(con.replace(':', str(self.line_index) + ':'))
                else:
                    self.new_con.append(con)
            else:
                self.new_con.append(con)
        self.content = self.new_con
        self.children = []
        self.context = []

    def parse(self):
        context = self.get_context(self.content, self.context)
        return context

    def get_context(self, content, context) -> tuple:
        for content in self.content:
            self.line_number = 0
            self.children = []
            new_tabno = 0
            self.alt_tab = 0
            # replace the spaces with tab spaces.
            new_content = content.replace('    ', '\t')
            # get the number of spaces in the new content.
            current_tabno = self.get_space_num(new_content)
            # create a new content list removing the current content.
            self.getter = self.content[self.content.index(content):]

            for new_c in self.getter:
                # create a new content for the children.
                cur_c = new_c.replace('    ', '\t')

                # get a new tab no for the preceeding text.
                new_tabno = self.get_space_num(cur_c)

                # print(new_c)
                # create a logic to fetch the item after each parent.
                if content == self.content[self.content.index(new_c) - 1] and self.content.index(
                        new_c) and new_tabno == current_tabno + 1 and self.is_comment(
                        content) == False:

                    # print(self.content[self.content.index(new_c) - 1])

                    # create a num of tabs for the detected child.
                    new_alt = new_c.replace('    ', '\t')

                    # get the whitespace num of tabs.
                    alt_tab = self.get_space_num(new_alt)

                    # create a new getter removing the current child.
                    self.new_getter = self.content[self.content.index(new_c):]

                    # loop through other children.
                    for child in self.new_getter:
                        # replace the spaces with tabs
                        new_cur_c = child.replace('    ', '\t')

                        # fetch the tab number for this item.
                        tabno = self.get_space_num(new_cur_c)

                        # run a complex system.
                        if tabno == alt_tab:
                            self.children.append(child.strip())
                        else:
                            # fix some issues concerning the parent.
                            if tabno < alt_tab:
                                break
            if self.is_class(content):
                item_dict = {
                    new_content.strip(): {"children": self.children, "line_no": str(self.content.index(content) + 1),
                                          "type": "class"}}
                context.append(item_dict)
            else:
                if self.children != []:
                    print(
                        f"""A property does'nt take any value or argumnets;\n\terror in line {self.content.index(content) + 1}""")
                else:
                    try:
                        if new_content.strip() != '' and new_content.strip().startswith('//') == False:
                            prop_type, value, name = self.get_value(new_content.strip())
                            property_dict = {name: {"value": value, "value-type": prop_type,
                                                    "line_no": str(self.content.index(content) + 1), "type": "property",
                                                    "actual-name": new_content.strip()}}
                            # print(property_dict)
                            context.append(property_dict)
                    except Exception as e:
                        print(f'Error fetching value in line {str(self.content.index(content) + 1)}')
                        # print(e)
                        continue
        return context

    def get_space_num(self, content):
        # get the number tabs in a content.
        num = 0
        for item in content:
            if item == '\t':
                num += 1
        return num

    def get_value(self, content):
        content_list = content.split()
        if ':' in content:
            for con in content_list:
                if con.endswith(':'):
                    new_con = self.filler(con)
                    new_content = content.replace(con, '').strip()
            prop_type = self.get_type(new_content)
            return (prop_type, self.fill_object(new_content), new_con)
        else:
            print("forgot a column in the property before your value!.")
            return ()

    def filler(self, content):
        chars = ['"', "'", ":", '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
        for char in chars:
            content = content.replace(char, '')
        return content

    def fill_object(self, content):
        chars = [':', '"', "'"]
        for char in chars:
            content = content.strip(char)
        return content

    def get_type(self, value):
        # Assigning types to property!
        if '\\' in value:
            return "PATH"
        elif '/' in value:
            return "PATH"
        elif value.isdigit():
            return "INT"
        elif 'true'.upper() in value.upper():
            return "BOOL"
        elif 'false'.upper() in value.upper():
            return "BOOL"
        elif '"' in value:
            return "STRING"
        elif "'" in value:
            return "STRING"
        elif '"""' in value:
            return "STRING"
        elif '`' in value:
            return "STRING"
        elif '=' in value:
            return "FUNCTION"
        elif '.' in value:
            return "FUNCTION"
        elif 'self' in value:
            return "FUNCTION"
        elif 'root' in value:
            return "FUNCTION"
        elif '()' in value:
            return "RUN_FUNCTION"
        else:
            return "UNKNOWN"

    def is_comment(self, content):
        # Check for comments in file!.
        if content.strip().startswith('//'):
            return True
        elif content.strip().startswith('#'):
            return True
        else:
            return False

    def is_class(self, content):
        # If the content passed looks like a class!.
        if content.strip() != '' and content.strip().startswith('//') == False:
            if content.strip()[0] == content.strip()[0].upper() and content.strip().endswith(':'):
                return True
            elif content.strip()[0] == content.strip()[0].upper() and content.strip().endswith(':') == False:
                print("Forgot a closing ':' ")
                return None
            else:
                return False