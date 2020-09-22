<!DOCTYPE html>


<html>
    <?php header("Access-Control-Allow-Origin: *"); ?>
    <head>
        <title>Page de crowdfunding</title>
        <link rel="stylesheet" href="style.css" />
        <meta charset="utf-8" />
    </head>
    <body>
        
        
        <?php 
            $id = $_GET['id'];
        ?>
        
        
        <div id="getImg">
        </div>
        
        <h2>Ici les utilisateurs vont voter sur ce que représente l'image :</h2>
        
        <form method="post" action="index.php?id=<?php echo $id ?>">
            <p>Réponse user 1 : </p><input type="text" name="AnswerUser1" required="required"/><br/>
            <p>Réponse user 2 : </p><input type="text" name="AnswerUser2" /><br/>
            <p>Réponse user 3 : </p><input type="text" name="AnswerUser3" /><br/>
            <p>Réponse user 4 : </p><input type="text" name="AnswerUser4" /><br/>
            <p>Réponse user 5 : </p><input type="text" name="AnswerUser5" /><br/>
            <p>Réponse user 6 : </p><input type="text" name="AnswerUser6" /><br/>
            <p>Réponse user 7 : </p><input type="text" name="AnswerUser7" /><br/>
            <p>Réponse user 8 : </p><input type="text" name="AnswerUser8" /><br/>
            <p>Réponse user 9 : </p><input type="text" name="AnswerUser9" /><br/>
            <p>Réponse user 10 : </p><input type="text" name="AnswerUser10" /><br/>
            <p>Réponse user 11 : </p><input type="text" name="AnswerUser11" /><br/>
            <p>Réponse user 12 : </p><input type="text" name="AnswerUser12" /><br/>
            <input type="submit" value="Valider" /><br/>
        </form>

        <?php
    
            
    
            //Si le formulaire a été envoyé, on a au moins une réponse d'utilisateur
            if($_POST['AnswerUser1'] != NULL)
            {
                $users = array($_POST['AnswerUser1'],$_POST['AnswerUser2'],$_POST['AnswerUser3'],$_POST['AnswerUser4'],$_POST['AnswerUser5'],
                $_POST['AnswerUser6'],$_POST['AnswerUser7'],$_POST['AnswerUser8'],$_POST['AnswerUser9'],$_POST['AnswerUser10'],
                $_POST['AnswerUser11'],$_POST['AnswerUser12']);
                $tab = array();
                foreach($users as $answer)
                {
                    if($answer != null)
                    {
                        array_push($tab,$answer);
                    }
                }
                
                
                echo $id;
                echo $answer = vote($tab);
                echo $nbrVotes = sizeof($tab);
                
                
                //Envois de la requête curl contenant la réponse vers l'API
                //API URL
                $url = 'http://localhost:3000/v1/answers';
                //create a new cURL resource
                $ch = curl_init($url);
                //setup request to send json via POST
                $data = array(
                    'id' => $id,
                    'answer' => $answer,
                    'nbrVotes' => $nbrVotes
                );
                $payload = json_encode($data);
                //attach encoded JSON string to the POST fields
                curl_setopt($ch, CURLOPT_POSTFIELDS, $payload);
                //set the content type to application/json
                curl_setopt($ch, CURLOPT_HTTPHEADER, array('Content-Type:application/json'));
                //return response instead of outputting
                curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
                //execute the POST request
                $result = curl_exec($ch);
                //close cURL resource
                curl_close($ch);
                
            }
        ?>


         
         <script src="js/ajax.js"></script>
         
        <script>
            const getImage = document.getElementById("getImg");
            ajaxGet("http://localhost:3000/v1/images/<?php echo $id ?>", function (reponse){
                const image = JSON.parse(reponse);
                const getIdElt = document.createElement("div");
                getIdElt.textContent = image.id;
                getIdElt.id = "id"
                const getImgElt = document.createElement("img");
                getImgElt.src = image.image;
                getImage.appendChild(getIdElt);
                getImage.appendChild(getImgElt);
            });


            const getAllId = document.getElementById("getAllId");
            ajaxGet("http://localhost:3000/v1/images", function (reponse){
                const ids = JSON.parse(reponse);
                ids.forEach(function (id) {
                    // Ajout du titre et du contenu de chaque article
                    var p = document.createElement("p");
                    var idElt = document.createElement("a");
                    idElt.href = "index.php?id=" + id.id;
                    idElt.textContent = id.id;
                    p.appendChild(idElt);
                    getAllId.appendChild(p);

                });
            });
        </script>
        
    </body>
</html>

<?php
    function compareName($tab, $nomImage)
    {
        foreach($tab as $answer)
        {
            if($answer != NULL && $answer == $nomImage)
            {
                return "Réponse trouvée !";
            } 
        }   
    }

    function vote($tab)
    {
        $max = 0;

        foreach($tab as $answer)
        {
            $tabCompteur = array();
            $tabCompteur = count(array_keys($tab,$answer)); 
            if($tabCompteur > $max)
            {
                $max = $tabCompteur;
            }
        }
        foreach($tab as $answer)
        {
            $tabCompteur = array();
            $tabCompteur = count(array_keys($tab,$answer)); 
            if($tabCompteur == $max)
            {
                return $answer;
            }
        }
    }

?>