from django.shortcuts import render
from django.http import HttpResponse
from apps.demo import task


# Create your views here.
"""##! Test-1
    ##* এখানে যদি এমন কোন task হত যা সম্পন্য করতে 10 seconds টাইম লাগতো 
    ##* তবে আমাদের ১০ সেকেন্ড Lodding screen দেখাবে then page load হবে
"""

# def test(request):
#     print("----------------------")
#     print("Result:-")

#     result = task.test_1(15, 25)

#     print("Results =", result)
#     print("----------------------")
#     return render(request, 'test.html')




"""##! Test-2
    ##* এখানে যদি যদিও Task টি সম্পন্য হতে ১০ সেকেন্ড টাইম লাগবে, 
    ##* তবে এখানে server relode হবার জন্যে ১০ সেকেন্ড অপেখ্যা করতে হবে না।
    ##! delay() অথাবা apply_async দুটি একি কাজ করে, তবে apply_async use করলে argument কে    
    ##! args=[15, 25] এবং kwargs=['name':'rakib', 'id':'25'] pass করতে হবে।

"""

# def test(request):
#     print("----------------------")
#     print("Result:-")
#     # result = task.test_2.delay(15, 25)
#     result1 = task.add.apply_async(args=[15, 25])
#     result2 = task.sub.apply_async(args=[25, 10])

#     print("Add Result =", result1)
#     print("Sub Result =", result2)
#     print("----------------------")
#     return render(request, 'test.html')



def test(request):
    if request.method == 'POST':
        num_1 = int(request.POST.get('number_1'))
        num_2 = int(request.POST.get('number_2'))

        # result = task.add.apply_async(args=[num_1, num_2])
        result = task.add.delay(num_1, num_2)

        data = {
            'result_id': result.id
        }
        return render(request, 'test.html', data)

    return render(request, 'test.html')



def result_view(request, task_id):
    result = task.add_result(task_id)

    ##! Task all Keys
    print("---------------------")
    print("Result ID =", task_id)
    print("Task ID   =", result.task_id)
    print("Task State  =", result.state)
    print("Task Sratus =", result.status)
    print("Task Result =", result.result)
    print("---------------------")

    # ##! Task all Methods
    # print("++++++++++++++++++++++")
    # print("Task Ready   =", result.ready())
    # print("Task Successfule  =", result.successful())
    # print("Task Failed =", result.failed())
    # # print("Task Get =", result.get())  ## এটা আমরা Use করবো না, এটা Use করলে Result না আসা পর্জন্ত Wait করা লাগে
    # print("++++++++++++++++++++++")

    data = {
        'result': result,
    }
    return render(request, 'result.html', data)



def start_task_view(request):
    initial_value = 10  # শুরু সংখ্যা
    increment_value = 2  # প্রতি ৫ সেকেন্ড পর পর যোগ করার সংখ্যা
    max_iterations  = 10  # যোগ করার পরিমাণ, এখানে ১০ বার যোগ করা হবে

    result = task.add_periodically.delay(initial_value, increment_value, max_iterations)

    return HttpResponse(f"Task ID: {result.id}")