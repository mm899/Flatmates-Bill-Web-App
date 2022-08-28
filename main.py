from flask.views import MethodView
from wtforms import Form, StringField, SubmitField
from flask import Flask, render_template, request
from flatmates_bill import flat

app = Flask(__name__)


class HomePage(MethodView):

    def get(self):
        return render_template('index.html')


class BillFormPage(MethodView):

    def get(self):
        bill_form = BillForm()
        return render_template('bill_form_page.html', billform=bill_form)

    def post(self):
        billform = BillForm(request.form)
        amount = float(billform.amount.data)
        period = billform.period.data
        flatmate1_name = billform.name1.data
        flatmate1_days_in_house = int(billform.days_in_house1.data)
        flatmate2_name = billform.name2.data
        flatmate2_days_in_house = int(billform.days_in_house2.data)

        the_bill = flat.Bill(amount=amount, period=period)
        flatmate1 = flat.Flatmate(flatmate1_name, flatmate1_days_in_house)
        flatmate2 = flat.Flatmate(flatmate2_name, flatmate2_days_in_house)

        amount1 = flatmate1.pays(the_bill, flatmate2)
        amount2 = flatmate2.pays(the_bill, flatmate1)

        return render_template('bill_form_page.html',
                               results=True,
                               billform=billform,
                               name1=flatmate1_name,
                               name2=flatmate2_name,
                               amount1=amount1,
                               amount2=amount2)


# class ResultsPage(MethodView):
#
#     def post(self):
#         billform = BillForm(request.form)
#         amount = float(billform.amount.data)
#         period = billform.period.data
#         flatmate1_name = billform.name1.data
#         flatmate1_days_in_house = int(billform.days_in_house1.data)
#         flatmate2_name = billform.name2.data
#         flatmate2_days_in_house = int(billform.days_in_house2.data)
#
#         the_bill = flat.Bill(amount=amount, period=period)
#         flatmate1 = flat.Flatmate(flatmate1_name, flatmate1_days_in_house)
#         flatmate2 = flat.Flatmate(flatmate2_name, flatmate2_days_in_house)
#
#         amount1 = flatmate1.pays(the_bill, flatmate2)
#         amount2 = flatmate2.pays(the_bill, flatmate1)
#
#         return render_template('results.html', name1=flatmate1_name, name2=flatmate2_name,
#                                amount1=amount1, amount2=amount2)


class BillForm(Form):
    amount = StringField("Bill Amount: ", default=100)
    period = StringField("Bill Period: ", default="January 1999")

    name1 = StringField("Name: ", default="John")
    days_in_house1 = StringField("Days in the house: ", default=15)

    name2 = StringField("Name: ", default="Mary")
    days_in_house2 = StringField("Days in the house: ", default=15)

    button = SubmitField("Calculate")


app.add_url_rule('/', view_func=HomePage.as_view('home_page'))
app.add_url_rule('/bill', view_func=BillFormPage.as_view('bill_form_page'))
# app.add_url_rule('/results', view_func=ResultsPage.as_view('results_page'))

app.run(debug=True)
