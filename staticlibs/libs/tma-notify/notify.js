/**

API pour pousser les notifications du navigateur. Ces notifications sont visibles sur toutes les fenêtres de browser.

Pour lancer une notification, utiliser dans un event la fonction pushNotification(title, tag, body)

TODO : Trouver une solution pour ne pas que la notification se ferme au bout de quelques secondes...

**/


function techmaNotification(title, tag, body) {

    var n = new Notification(title,  {
        icon: '',
        tag: tag,
        body: body,
        requireInteraction: true,
        silent: false,
        sticky: trues
    });
}

// When the button is clicked
function pushNotification(title, tag, body) {

    // If notifications are granted show the notification
    if (Notification && Notification.permission === "granted") {
        techmaNotification(title, tag, body);
    }

    // If they are not denied (i.e. default)
    else if (Notification && Notification.permission !== "denied") {

        // Request permission
        Notification.requestPermission(function (status) {

            // Change based on user's decision
            if (Notification.permission !== status) {
                Notification.permission = status;
            }

            // If it's granted show the notification
            if (status === "granted") {

                techmaNotification(title, tag, body);
            }
        });

    }
}
