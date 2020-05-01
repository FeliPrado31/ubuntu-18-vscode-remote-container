class Identifiers:
    class recv:
        class Old_Protocol:
            C = 1
            Old_Protocol = 1
        
        class Sync:
            C = 4
            Object_Sync = 3
            Mouse_Movement = 4
            Mort = 5
            Player_Position = 6
            Shaman_Position = 8
            Crouch = 9
            Consumable_Object = 16
        
        class Room:
            C = 5
            Map_26 = 8
            Shaman_Message = 9
            Convert_Skill = 14
            Demolition_Skill = 15
            Projection_Skill = 16
            Enter_Hole = 18
            Get_Cheese = 19
            Place_Object = 20
            Ice_Cube = 21
            Bridge_Break = 24
            Defilante_Points = 25
            Restorative_Skill = 26
            Recycling_Skill = 27
            Gravitational_Skill = 28
            Antigravity_Skill = 29
            Handymouse_Skill = 35
            Enter_Room = 38
            Room_Password = 39
            Send_Music = 70
            Music_Time = 71
            Send_PlayList = 73
        
        class Chat:
            C = 6
            Chat_Message = 6
            Staff_Chat = 10
            Commands = 26
        
        class Player:
            C = 8
            Emote = 1
            Langue = 2
            Emotions = 5
            Shaman_Fly = 15
            Shop_List = 20
            Buy_Skill = 21
            Redistribute = 22
            Report = 25
            Ping = 30
            Meep = 39
            Vampire = 66
        
        class Buy_Fraises:
            C = 12
            Buy_Fraises = 10
        
        class Tribe:
            C = 16
            Tribe_House = 1
            Tribe_Invite = 2
        
        class Shop:
            C = 20
            Equip_Clothe = 6
            Save_Clothe = 7
            Info = 15
            Equip_Item = 18
            Buy_Item = 19
            Buy_Custom = 20
            Custom_Item = 21
            Buy_Clothe = 22
            Buy_Shaman_Item = 23
            Equip_Shaman_Item = 24
            Buy_Shaman_Custom = 25
            Custom_Shaman_Item = 26
            Send_Gift = 28
            Gift_Result = 29
        
        class Modopwet:
            C = 25
            Modopwet = 2
            Delete_Report = 23
            Watch = 24
            Ban_Hack = 25
            Change_Langue = 26
            Chat_Log = 27
        
        class Login:
            C = 26
            Create_Account = 7
            Login = 8
            Player_FPS = 13
            Captcha = 20
            Player_Info = 28
            Player_Info2 = 29
            Rooms_List = 35
            Request_Info = 40
        
        class Transformation:
            C = 27
            Transformation_Object = 11
        
        class Informations:
            C = 28
            Game_Log = 4
            Player_Ping = 6
            Change_Shaman_Type = 10
            Letter = 15
            Send_Gift = 16
            Computer_Info = 17
            Change_Shaman_Color = 18
            Informations = 50
        
        class Lua:
            C = 29
            Lua_Script = 1
            Key_Board = 2
            Mouse_Click = 3
            Popup_Answer = 20
            Text_Area_Callback = 21
            Color_Picked = 32
        
        class Cafe:
            C = 30
            Mulodrome_Close = 13
            Mulodrome_Join = 15
            Mulodrome_Leave = 17
            Mulodrome_Play = 20
            Reload_Cafe = 40
            Open_Cafe_Topic = 41
            Create_New_Cafe_Post = 43
            Create_New_Cafe_Topic = 44
            Open_Cafe = 45
            Vote_Cafe_Post = 46
        
        class Inventory:
            C = 31
            Open_Inventory = 1
            Use_Consumable = 3
            Equip_Consumable = 4
            Trade_Invite = 5
            Cancel_Trade = 6
            Trade_Add_Consusmable = 8
            Trade_Result = 9
        
        class Tribulle:
            C = 60
            Tribulle = 3

        class Transformice:
            C = 100
            Invocation = 2
            Remove_Invocation = 3
            Paint_Consumable = 40
            Change_Shaman_Badge = 79
            Map_Info = 80
            Bots_Village = 75
    
    class send:
        Sync = [4, 3]
        Player_Movement = [4, 4]
        Move_Object = [4, 7]
        Player_Position = [4, 6]
        Remove_Object = [4, 8]
        Crouch = [4, 9]
        Shaman_Position = [4, 10]
        
        Rounds_Count = [5, 1]
        New_Map = [5, 2]
        Shaman_Message = [5, 9]
        Map_Start_Timer = [5, 10]
        Convert_Skill = [5, 13]
        Skill_Object = [5, 14]
        Demolition_Skill = [5, 15]
        Projection_Skill = [5, 16]
        Spawn_Object = [5, 20]
        Enter_Room = [5, 21]
        Round_Time = [5, 22]
        Snow = [5, 23]
        Bridge_Break = [5, 24]
        Restorative_Skill = [5, 26]
        Recycling_Skill = [5, 27]
        Gravitation_Skill = [5, 28]
        Antigravity_Skill = [5, 29]
        Rollout_Mouse_Skill = [5, 30]
        Mouse_Size = [5, 31]
        Remove_All_Objects_Skill = [5, 32]
        Leaf_Mouse_Skill = [5, 33]
        Iced_Mouse_Skill = [5, 34]
        Handymouse_Skill = [5, 35]
        Spider_Mouse_Skill = [5, 36]
        Grapnel_Mouse_Skill = [5, 37]
        Evolution_Skill = [5, 38]
        Room_Password = [5, 39]
        Skill = [5, 40]
        Reset_Shaman_Skills = [5, 42]
        Gatman_Skill = [5, 43]
        Bonfire_Skill = [5, 45]
        Soulmate = [5, 48]
        Teleport = [5, 50]
        Music_Video = [5, 72]
        Music_PlayList = [5, 73]
        Tutorial = [5, 90]
        Authent = [67, 28]
        Undefined = [20, 4]
        
        Chat_Message = [6, 6]
        Message = [6, 9]
        Staff_Chat = [6, 10]
        Recv_Message = [6, 20]
        
        Room_Server = [7, 1]
        Room_Type = [7, 30]
        
        Player_Emote = [8, 1]
        Give_Currency = [8, 2]
        Move_Player = [8, 3]
        Emotion = [8, 5]
        Player_Win = [8, 6]
        Set_Player_Score = [8, 7]
        Shaman_Exp = [8, 8]
        Shaman_Gain_Exp = [8, 9]
        Enable_Skill = [8, 10]
        Shaman_Info = [8, 11]
        New_Shaman = [8, 12]
        Titles_List = [8, 14]
        Shaman_Fly = [8, 15]
        Profile = [8, 16]
        Remove_Cheese = [8, 19]
        Shop_List = [8, 20]
        Shaman_Skills = [8, 22]
        NPC = [8, 30]
        Meep = [8, 38]
        Can_Meep = [8, 39]
        Unlocked_Badge = [8, 42]
        Anim_Zelda = [8, 44]
        Mouse_Freeze = [8, 45]
        Vampire_Mode = [8, 66]
        
        Banner_Login = [16, 9]
        Interface_Login = [100, 99]
        
        Item_Buy = [20, 2]
        Promotion = [20, 3]
        Undefined = [20, 4]
        Shop_Info = [20, 15]
        Look_Change = [20, 17]
        Shaman_Look = [20, 24]
        Shaman_Items = [20, 27]
        Gift_Result = [20, 29]
        Shop_Gift = [20, 30]
        
        Shaman_Earned_Exp = [24, 1]
        Shaman_Earned_Level = [24, 2]
        Redistribute_Error_Time = [24, 3]
        Redistribute_Error_Cheeses = [24, 4]
        
        Open_Modopwet = [25, 2]
        Modopwet_Banned = [25, 5]
        Modopwet_Disconnected = [25, 6]
        Modopwet_Deleted = [25, 7]
        Modopwet_Chatlog = [25, 10]
        Watch = [25, 11]
        
        Gain_Give = [26, 1]
        Player_Identification = [26, 2]
        Correct_Version = [26, 3]
        First_Count = [26, 10]
        Player_Damanged = [26, 11]
        Login_Result = [26, 12]
        Captcha = [26, 20]
        Ping = [26, 26]
        Images = [26, 31]
        Login_Souris = [26, 33]
        Game_Mode = [26, 35]
        Tribulle_Token = [26, 41]
        
        Can_Transformation = [27, 10]
        Transformation = [27, 11]
        
        Time_Stamp = [28, 2]
        Promotion_Popup = [28, 3]
        Message_Langue = [28, 5]
        Player_Ping = [28, 6]
        Shaman_Type = [28, 10]
        Send_Gift = [28, 12]
        Email_Confirmed = [28, 13]
        Letter = [28, 15]
        Take_Cheese = [28, 41]
        Log_Message = [28, 46]
        Request_Info = [28, 50]
        Server_Restart = [28, 88]

        Bind_Key_Board = [29, 2]
        Bind_Mouse = [29, 3]
        Set_Name_Color = [29, 4]
        Lua_Message = [29, 6]
        Add_Text_Area = [29, 20]
        Update_Text_Area = [29, 21]
        Remove_Text_Area = [29, 22]
        Add_Popup = [29, 23]
        Add_Physic_Object = [29, 28]
        Show_Color_Picker = [29, 32]
        
        Mulodrome_Result = [30, 4]
        Mulodrome_End = [30, 13]
        Mulodrome_Start = [30, 14]
        Mulodrome_Join = [30, 15]
        Mulodrome_Leave = [30, 16]
        Mulodrome_Winner = [30, 21]
        Cafe_Topics_List = [30, 40]
        Open_Cafe_Topic = [30, 41]
        Open_Cafe = [30, 42]
        Cafe_New_Post = [30, 44]
        
        Inventory = [31, 1]
        Update_Inventory_Consumable = [31, 2]
        Use_Inventory_Consumable = [31, 3]
        Trade_Invite = [31, 5]
        Trade_Result = [31, 6]
        Trade_Start = [31, 7]
        Trade_Add_Consumable = [31, 8]
        Trade_Confirm = [31, 9]
        Trade_Close = [31, 10]
        
        Bulle = [44, 1]
        Bulle_ID = [44, 22]
        
        Old_Tribulle = [60, 1]
        Tribulle = [60, 3]
        New_Tribulle = [60, 4]

        Invocation = [100, 2]
        Remove_Invocation = [100, 3]
        Joquempo = [100, 5]
        Crazzy_Packet = [100, 40]
        New_Consumable = [100, 67]
        Add_Anim = [100, 68]
        Add_Frame = [100, 69]
        Pet = [100, 70]
        Balloon_Badge = [100, 71]
        Change_Title = [100, 72]
        
        Players_List = [144, 1]
        Player_Respawn = [144, 2]
        Player_Get_Cheese = [144, 6]
    
    class old:
        class recv:
            class Player:
                C = 4
                Bomb_Explode = 6
                Conjure_Start = 12
                Conjure_End = 13
                Conjuration = 14
                Snow_Ball = 16
            
            class Room:
                C = 5
                Anchors = 7
                Begin_Spawn = 8
                Spawn_Cancel = 9
                Totem_Anchors = 13
                Move_Cheese = 16
                Bombs = 17
            
            class Balloons:
                C = 8
                Place_Balloon = 16
                Remove_Balloon = 17
            
            class Map:
                C = 14
                Vote_Map = 4
                Load_Map = 6
                Validate_Map = 10
                Map_Xml = 11
                Return_To_Editor = 14
                Export_Map = 18
                Reset_Map = 19
                Exit_Editor = 26
            
            class Draw:
                C = 25
                Clear = 3
                Drawing = 4
                Point = 5
            
            class Dummy:
                C = 26
                Dummy = 2

        class send:
            Bomb_Explode = [4, 6]
            Conjure_Start = [4, 12]
            Conjure_End = [4, 13]
            Add_Conjuration = [4, 14]
            Conjuration_Destroy = [4, 15]
            
            Anchors = [5, 7]
            Begin_Spawn = [5, 8]
            Spawn_Cancel = [5, 9]
            Move_Cheese = [5, 16]
            Bombs = [5, 17]
            Player_Get_Cheese = [5, 19]
            Gravity = [5, 22]
            
            Player_Died = [8, 5]
            Player_Disconnect = [8, 7]
            Player_Respawn = [8, 8]
            Player_List = [8, 9]
            Change_Title = [8, 13]
            Unlocked_Title = [8, 14]
            Titles_List = [8, 15]
            Balloon = [8, 16]
            Shaman_Perfomance = [8, 17]
            Save_Remaining = [8, 18]
            Sync = [8, 21]
            Catch_The_Cheese_Map = [8, 23]
            
            Vote_Box = [14, 4]
            Map_Exported = [14, 5]
            Load_Map_Result = [14, 8]
            Load_Map = [14, 9]
            Map_Editor = [14, 14]
            Map_Validated = [14, 17]
            Editor_Message = [14, 20]
            
            Change_Tribe_Code_Result = [16, 4]
            
            Totem = [22, 22]
            
            Drawing_Clear = [25, 3]
            Drawing = [25, 4]
            Drawing_Point = [25, 5]
            
            Player_Ban_Message = [26, 7]
            Login = [26, 8]
            Ban_Consideration = [26, 9]
            Music = [26, 12]
            Player_Ban = [26, 17]
            Player_Ban_Login = [26, 18]
            Log = [26, 23]
            
            Totem_Item_Count = [28, 11]