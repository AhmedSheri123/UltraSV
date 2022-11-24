from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='dashboardMain'),
    path('Settings', views.Settings, name='Settings'),

    #service
    path('mySotre', views.mySotre, name='mySotre'),
    path('myServices/<int:ServiesTypeId>', views.myServices, name="myServices"),
    path('AddNewServiceForMe/<int:store_id>', views.AddNewServiceForMe, name="AddNewServiceForMe"),
    path('DeleteMyService/<int:id>', views.DeleteMyService, name='DeleteMyService'),
    path('EditServiceForMe/<int:service_id>', views.EditServiceForMe, name="EditServiceForMe"),
    path('admin/RequestsUnderReview', views.RequestsUnderReview, name='RequestsUnderReview'),

    #Services added UnderReview
    path('admin/requestsUnderReviewServices', views.requestsUnderReviewServices, name='requestsUnderReviewServices'),
    path('admin/requestsUnderReviewServicesAccept/<int:WaitForAcceptID>', views.requestsUnderReviewServicesAccept, name='requestsUnderReviewServicesAccept'),
    path('admin/requestsUnderReviewSrvicesCancel/<int:WaitForAcceptID>', views.requestsUnderReviewSrvicesCancel, name='requestsUnderReviewSrvicesCancel'),

    #Services edited UnderReview
    path('admin/requestsUnderReviewEditedServices', views.requestsUnderReviewEditedServices, name='requestsUnderReviewEditedServices'),
    path('admin/requestsUnderReviewEditedServicesAccept/<int:WaitForAcceptID>', views.requestsUnderReviewEditedServicesAccept, name='requestsUnderReviewEditedServicesAccept'),
    path('admin/requestsUnderReviewEditedSrvicesCancel/<int:WaitForAcceptID>', views.requestsUnderReviewEditedSrvicesCancel, name='requestsUnderReviewEditedSrvicesCancel'),




    #blog
    path('myBlog', views.myBlog, name='myBlog'),
    path('myArticles/<int:ArticleTypeId>', views.myArticles, name="myArticles"),
    path('DeleteMyArticle/<int:id>', views.DeleteMyArticle, name='DeleteMyArticle'),
    path('AddNewArticleForMe/<int:blog_id>', views.AddNewArticleForMe, name="AddNewArticleForMe"),
    path('EditArticleForMe/<int:service_id>', views.EditArticleForMe, name="EditArticleForMe"),

    #Areticls added UnderReview
    path('admin/requestsUnderReviewAreticls', views.requestsUnderReviewAreticls, name='requestsUnderReviewAreticls'),
    path('admin/requestsUnderReviewAreticlsAccept/<int:WaitForAcceptID>', views.requestsUnderReviewAreticlsAccept, name='requestsUnderReviewAreticlsAccept'),
    path('admin/requestsUnderReviewAreticlsCancel/<int:WaitForAcceptID>', views.requestsUnderReviewAreticlsCancel, name='requestsUnderReviewAreticlsCancel'),

    #Areticl edited UnderReview
    path('admin/requestsUnderReviewEditedAreticls', views.requestsUnderReviewEditedAreticls, name='requestsUnderReviewEditedAreticls'),
    path('admin/requestsUnderReviewEditedAreticlsAccept/<int:WaitForAcceptID>', views.requestsUnderReviewEditedAreticlsAccept, name='requestsUnderReviewEditedAreticlsAccept'),
    path('admin/requestsUnderReviewEditedAreticlsCancel/<int:WaitForAcceptID>', views.requestsUnderReviewEditedAreticlsCancel, name='requestsUnderReviewEditedAreticlsCancel'),

    
    path('Withdrawn', views.Withdrawn, name='Withdrawn'),
    path('dashboardWithdraw', views.dashboardWithdraw, name='dashboardWithdraw'),
    path('WithdrawAccept/<int:id>', views.WithdrawAccept, name='WithdrawAccept'),
    path('WithdrawCancel/<int:id>', views.WithdrawCancel, name='WithdrawCancel'),
    path('WithdrawComplete/<int:id>', views.WithdrawComplete, name='WithdrawComplete'),
    path('WithdrawDelete/<int:id>', views.WithdrawDelete, name='WithdrawDelete'),
    ]
    
    