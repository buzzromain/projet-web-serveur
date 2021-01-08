$(() => {
    function createComment(event) {
        event.preventDefault();

        if ($("#create-comment-body").val() != "") {
            const data = new FormData(document.getElementById("create-comment-form"));
            $.ajax({
                url: $("#create-comment-form").attr('action'),
                type: 'POST',
                processData: false,
                contentType: false,
                data: data,
                dataType: 'json',
                success: function (data) {
                    let formattedDate = moment(data.created_at);
                    formattedDate.localeData("fr-FR");
                    formattedDate = formattedDate.format("DD MMMM YYYY")

                    const newComment = $(
                    `
                    <div class="shadow p-3 mb-3 bg-white rounded comments-container">
                        <div class="d-flex justify-content-between comment-meta-container">
                        <span><a href="/users/${data.author.id}">${data.author.username}</a><small> <i>
                        ${'le ' + formattedDate}</i></small></span>
                        
                        <div class="btn-group">
                            <a role="button" href="/posts/${data.post.id}/comments/${data.id}" class="btn btn-secondary btn-sm"><i class="fas fa-external-link-alt"></i></a>
                            <button type="button" data-uri="/posts/${data.post.id}/comments/${data.id}" class="btn btn-danger btn-sm delete-comment-button" ><i class="fas fa-trash-alt fa-sm" aria-hidden="true"></i></button>
                            <button type="button" data-uri="/posts/${data.post.id}/comments/${data.id}" class="btn btn-primary btn-sm edit-comment-button"><i class="fas fa-edit fa-sm" aria-hidden="true"></i></button>
                            ${$('a[href="/posts/create"]').length > 0 ? '': '<button type="button" class="btn btn-secondary btn-sm"><i class="fas fa-user-slash fa-sm" aria-hidden="true"></i></button>'}
                        </div>
    
                    </div>
                        <p class="comment-body">${data.body}</p>
                    </div>
                    `
                    )
                    newComment.find('.edit-comment-button').on('click', editComment);
                    newComment.find('.delete-comment-button').on('click', deleteComment);
                    const successAlert = $(
                        `
                        <div class="alert alert-success success-create-comment-alert" role="alert">
                        Commentaire publié avec succès
                        </div>
                    `
                    )
                    successAlert.insertBefore("#create-comment-form");
                    newComment.insertBefore("#create-comment-form");
                    $(".success-create-comment-alert").delay(1500).slideUp(300, function () {
                        $(this).alert('close');
                    });
                    $("#create-comment-form").trigger('reset');
                },
                error: function () {
                    const failAlert = $(
                        `
                        <div class="alert alert-danger fail-create-comment-alert" role="alert">
                        Impossible de publier le commentaire. Veuillez réessayer plus tard.
                        </div>
                        `
                    )
                    failAlert.insertBefore("#create-comment-form");
                    $(".fail-create-comment-alert").delay(1500).slideUp(300, function () {
                        $(this).alert('close');
                    });
                }
            });
        }
    }
    
    function deletePost(event) {
        $.ajax({
            url: $("#delete-post-button").attr('data-uri'),
            type: 'DELETE',
            dataType: 'text',
            success: function (data) {
                console.log("OK");
                location.href = '/posts'
            },
            error: function () {
                const failAlert = $(
                    `
                    <div class="alert alert-danger fail-delete-post-alert" role="alert">
                    Impossible de supprimer l'article. Veuillez réessayer plus tard.
                    </div>
                `
                )
                $('#delete-post-modal').modal('toggle');
                failAlert.insertBefore("#post-title");
                $(".fail-delete-post-alert").delay(1500).slideUp(300, function () {
                    $(this).alert('close');
                });
            }
        });
    }

    function editPostButton(event) {
        $("#new-post-title").val($("#post-title").text());
        $("#new-post-body").val($("#post-body").text().trim());
    }

    function editPost(event) {
        event.preventDefault();
        const data = {
            'title': $("#new-post-title").val(),
            'body': $("#new-post-body").val().trim()
        }
        $.ajax({
            url: $("#edit-post").attr('data-uri'),
            type: 'PUT',
            data: JSON.stringify(data),
            contentType: "application/json",
            success: function (data) {
                $("#post-title").text(data.title);
                $("#post-body").text(data.body);
                $('#edit-post-modal').modal('toggle');
            },
            error: function () {
                const failAlert = $(
                    `
                    <div class="alert alert-danger fail-delete-post-alert" role="alert">
                    Impossible de modifier l'article. Veuillez réessayer plus tard.
                    </div>
                `
                )
                $('#edit-post-modal').modal('toggle');
                failAlert.insertBefore("#post-title");
                $(".fail-delete-post-alert").delay(1500).slideUp(300, function () {
                    $(this).alert('close');
                });
            }
        });
    }

    function editComment() {
        const uri = $(this).attr("data-uri");
        const commentElm = $(this).parent().parent().parent();
        const commentBodyElm = commentElm.find('.comment-body');
        const commentBtnGroup = commentElm.find('.btn-group');
        const commentBody = commentBodyElm.text().trim();
        commentBodyElm.hide();
        commentBtnGroup.hide();
        commentElm.append(`
        <textarea class="form-control" name="new-comment-body">
        </textarea>
        <button type="button" class="btn btn-light btn-sm" id="cancel-edit-button">Annuler</button>
        <button class="btn btn-primary btn-sm" id="edit-button-submit">Actualiser</button>
        `);
        commentElm.children('cancel-edit-button').on("click", (event) => {
            textAreaElm.remove();
            commentElm.children('button').remove();
            commentBodyElm.text(data.body);
            commentBodyElm.show();
            commentBtnGroup.show();
        });

        const textAreaElm = commentElm.children('textarea');
        textAreaElm.val(commentBodyElm.text().trim());
        commentElm.children('button').on("click", (event) => {
            event.preventDefault();
            const data = {
                'body': textAreaElm.val().trim(),
            }
            console.log(data);
            $.ajax({
                url: uri,
                type: 'PUT',
                data: JSON.stringify(data),
                contentType: "application/json",
                success: function (data) {
                    textAreaElm.remove();
                    commentElm.children('button').remove();
                    commentBodyElm.text(data.body);
                    commentBodyElm.show();
                    commentBtnGroup.show();
                },
                error: function () {
                    textAreaElm.remove();
                    commentElm.children('button').remove();
                    commentBodyElm.show();
                    commentBtnGroup.show();
                    const failAlert = $(
                        `
                        <div class="alert alert-danger fail-delete-post-alert" role="alert">
                        Impossible de modifier le commentaire. Veuillez réessayer plus tard.
                        </div>
                    `
                    )
                    failAlert.insertBefore("#create-comment-form");
                    $(".fail-delete-post-alert").delay(1500).slideUp(300, function () {
                        $(this).alert('close');
                    });
                }
            });
        });
    }

    function deleteComment() {
        const commentElm = $(this).parent().parent().parent();
        $.ajax({
            url: $(this).attr('data-uri'),
            type: 'DELETE',
            dataType: 'text',
            success: function (data) {
                commentElm.remove();
                const successAlert = $(
                `
                    <div class="alert alert-success success-create-comment-alert" role="alert">
                    Commentaire supprimé avec succès
                    </div>
                `
                )
                successAlert.insertBefore("#create-comment-form");
                
                $(".success-create-comment-alert").delay(1500).slideUp(300, function () {
                    $(this).alert('close');
                });

            },
            error: function () {
                const failAlert = $(
                    `
                        <div class="alert alert-danger fail-create-comment-alert" role="alert">
                        Impossible de supprimer le commentaire. Veuillez réessayer plus tard.
                        </div>
                    `
                )
                failAlert.insertBefore("#create-comment-form");
                
                $(".fail-create-comment-alert").delay(1500).slideUp(300, function () {
                    $(this).alert('close');
                });
            }
        });
    }

    function banUser() {
        $.ajax({
            url: $(this).attr('data-uri'),
            type: 'PATCH',
            dataType: 'json',
            data: JSON.stringify({"is_banned": true}),
            contentType: "application/json",
            success: function (data) {
                const successAlert = $(
                `
                    <div class="alert alert-success success-ban-user-alert" role="alert">
                    Utilisateur banni avec succès
                    </div>
                `
                )
                successAlert.insertBefore("#create-comment-form");
                
                $(".success-ban-user-alert").delay(1500).slideUp(300, function () {
                    $(this).alert('close');
                });

            },
            error: function () {
                const failAlert = $(
                    `
                        <div class="alert alert-danger fail-ban-user-alert" role="alert">
                        Impossible de bannir cet utilisateur. Veuillez réessayer plus tard.
                        </div>
                    `
                )
                failAlert.insertBefore("#create-comment-form");
                
                $(".fail-ban-user-alert").delay(1500).slideUp(300, function () {
                    $(this).alert('close');
                });
            }
        });
    }

    function upgradeUser(event) {
        event.preventDefault();
        const username = $("#user-list").val();
        const currentOption = $(`option[value=${username}`);
        const userId = currentOption.attr('data-id');
        console.log($(this));
        $.ajax({
            url: 'users/' + userId,
            type: 'PATCH',
            dataType: 'json',
            data: JSON.stringify({"is_admin": true}),
            contentType: "application/json",
            success: function (data) {
                const successAlert = $(
                `
                    <div class="alert alert-success success-upgrande-user-alert" role="alert">
                    Changement de role de l'utilisateur avec succès.
                    </div>
                `
                )
                successAlert.insertAfter("#upgrade-user");
                
                $(".success-upgrande-user-alert").delay(1500).slideUp(300, function () {
                    $(this).alert('close');
                });
                currentOption.remove();
            },
            error: function () {
                const failAlert = $(
                    `
                        <div class="alert alert-danger fail-upgrade-user-alert" role="alert">
                        Impossible de mettre cet utilisateur en tant qu'administrateur. Veuillez réessayer plus tard.
                        </div>
                    `
                )
                failAlert.insertAfter("#upgrade-user");
                
                $(".fail-upgrade-user-alert").delay(1500).slideUp(300, function () {
                    $(this).alert('close');
                });
            }
        });
    }

    $("#create-comment-form").on("submit", createComment);
    $("#delete-post-button").on("click", deletePost);
    $("#edit-post-button").on("click", editPostButton);
    $("#edit-post").on("submit", editPost);
    $(".edit-comment-button").on('click', editComment);
    $(".delete-comment-button").on('click', deleteComment);
    $(".ban-user-button").on('click', banUser);
    $("#upgrade-user").on('submit', upgradeUser);
});