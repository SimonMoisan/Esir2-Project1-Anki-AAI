<!DOCTYPE html>
<html>
    <head>
        <title>Page de crowdfunding</title>
        <link rel="stylesheet" href="style.css" />
        <meta charset="utf-8" />
    </head>
    <body>
        <h1>Page de test de reconnaissance d'image avec Crowdfunding</h1>
        
        <h2>Récapitulatif des versions du site (version actuelle = version 1) : <br/></h2>
        <p>
            Version 0 :<br/>
            Cette page a pour but de générer une image avec un champ de réponse permettant de définir <br/>
            ce que contient l'image. Dans cette version 3 utilisateurs peuvent répondre, il dois y avoir <br/>
            au moins un premier utilisateur à répondre pour envoyer le formulaire. Si une réponse envoyeée <br/>
            correspond au nom de l'image, on envois une réponse positive.<br/>
            <br/>
        </p>
        <p>
            Version 1 :<br/>
            Dans cette version, on donne la réponse la plus récurente.
        </p>
        
        
        <?php 
            $nomImage = "panda";
        ?>
        
        <img src="images/<?php echo $nomImage ?>.jpg" alt="Photo à deviner" />
        
        <form method="post" action="index.php">
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
                
                echo "<br/>Formulaire envoyé <br/>";
                //echo compareName($tab, $nomImage);
                echo vote($tab);
            }
        ?>


         
         <!--<script src="js/ajax.js"></script>
         <script src="js/cours.js"></script>-->
        
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