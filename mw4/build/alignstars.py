
############################################################
# -*- coding: utf-8 -*-
#
#       #   #  #   #   #    #
#      ##  ##  #  ##  #    #
#     # # # #  # # # #    #  #
#    #  ##  #  ##  ##    ######
#   #   #   #  #   #       #
#
# Python-based Tool for interaction with the 10micron mounts
# GUI with PyQT5 for python
# Python  v3.6.7
#
# Michael Würtenberger
# (c) 2018
#
# Licence APL2.0
#
###########################################################
#
# this file is auto generated for the purpose of getting data prepared
# to show the alignment stars in mountwizzard
#
# standard libraries
# external packages
# local import


def generateAlignStars():
    """
    generateAlignStars is the function where the alignment stars which were present in the 
    mount computer from hipparcos catalogue are stored. for a correct calculation we need 
    beside the J2000 coordinated the proper motion in ra and dec, the parallax and the 
    radial velocity as the stars move over time. the data is calculated from the hipparcos 
    catalogue using skyfield library
    
    the data is written in 
    [name, hip no, ra, dec, ra proper motion, dec proper motion, parallax, radial velocity]
    based on J2000 epoch.
    the units are fitting erfa needs:
    [str, int, radians, radians, radians / year, radians/year, arc sec, km /s]
    
    
    """
    
    star = dict()
    star['Achernar'] = [0.42636313743386084, -0.9989721040992605, 4.267359632399454e-07,
                        -1.9431237114262957e-07, 0.022680000001570513, 4.512483521476569e-05]
    star['Acrux'] = [3.257647500944081, -1.1012877251083137, -1.7147915360582993e-07,
                     -7.141291885025191e-08, 0.010169999999992536, 0.00018371089505169385]
    star['Adhara'] = [1.8265998141713244, -0.5056581249237073, 1.2750598011628168e-08,
                      1.1102234088793558e-08, 0.007569999999999877, 7.259912285180442e-06]
    star['Agena'] = [3.6818723020537076, -1.053709711449934, -1.6464353444471552e-07,
                     -1.2149417463462386e-07, 0.006210000000391972, 3.869200910092055e-05]
    star['Albireo'] = [5.108235120230585, 0.48798817964093627, -3.437327854555683e-08,
                       -2.729501586886459e-08, 0.008460000000030304, 2.2136709851271847e-06]
    star['Alcor'] = [3.5134663322179307, 0.9597199664899241, 5.834716928472566e-07,
                     -8.212927581831126e-08, 0.04018999999968475, 0.00015050914068354885]
    star['Aldebaran'] = [1.203934427163616, 0.2881311174431596, 3.043641257300601e-07,
                         -9.180434764560061e-07, 0.05009000001432034, 0.00020814887348950727]
    star['Alderamin'] = [5.578863965233713, 1.092326995350734, 7.267917254309235e-07,
                         2.3401708309557666e-07, 0.06684000000238877, 2.8028645656872635e-05]
    star['Algenib'] = [0.8915279133021705, 0.8702403038092067, 1.1688817634374709e-07,
                       -1.261001153321045e-07, 0.0055099999999921505, 0.0011773710216326351]
    star['Algieba'] = [2.7051579856054455, 0.34629079011542624, 1.5066462158990716e-06,
                       -7.411914831687442e-07, 0.025960000043547513, 0.0011070442873128607]
    star['Algol'] = [0.821041669739561, 0.7148108194311975, 1.1587045365003386e-08,
                     -6.981317771675758e-09, 0.03514000000000205, 4.006764477186861e-08]
    star['Alhena'] = [1.7353444804301865, 0.28621721715159426, -9.890177392282037e-09,
                      -3.2443731569840854e-07, 0.0311200000017577, 3.8035452502109436e-05]
    star['Alioth'] = [3.3773455494099123, 0.9766826272095643, 5.417300039981641e-07,
                      -4.358631414718114e-08, 0.04030000000150908, 2.616754603602984e-05]
    star['Alkaid'] = [3.6108204064416527, 0.8606779733601759, -5.877384404033237e-07,
                      -7.54389709946754e-08, 0.03239000000253164, 5.290086966817523e-05]
    star['Almach'] = [0.5406147230070784, 0.7387902351417366, 2.088566559814505e-07,
                      -2.465280063745504e-07, 0.00919000000153429, 0.0001034513542215724]
    star['Alnair'] = [5.795517277320005, -0.8196318811189315, 6.186331748246424e-07,
                      -7.17085722055635e-07, 0.03216000001150597, 0.00024192618143056515]
    star['Alnilam'] = [1.4670084744903535, -0.020977517366786498, 7.223723866431384e-09,
                       -5.1390250071863436e-09, 0.0024300000000014596, 3.63278081867269e-07]
    star['Alnitak'] = [1.4868409136424068, -0.033904139982525006, 1.9344065690593402e-08,
                       1.231426764584966e-08, 0.003990000000009708, 1.4795031132829625e-06]
    star['Alphard'] = [2.476566370696421, -0.1511192705234524, -7.024946272310793e-08,
                       1.6120055731978998e-07, 0.018399999999962578, 0.00016391728372232186]
    star['Alphecca'] = [4.078351611721369, 0.46625436926948094, 5.836157823581908e-07,
                        -4.3361892800692933e-07, 0.043650000007291134, 0.00011835310422146781]
    star['Alpheratz'] = [0.036605554597617405, 0.5077147413037055, 6.577885543330571e-07,
                         -7.90006001232231e-07, 0.03359999999788266, 0.0016673676990050404]
    star['Altair'] = [5.195802293942589, 0.15480289564215213, 2.602594244171653e-06,
                      1.869138807384765e-06, 0.19444000005964884, 0.0005839765784371194]
    star['Aludra'] = [1.9377299602552602, -0.5114352678961788, -1.822898669637355e-08,
                      3.228859257622338e-08, 0.001019999999999913, 0.001999429413248187]
    star['Ankaa'] = [0.11469934998473073, -0.7383983714315256, 1.1284927917001944e-06,
                     -1.7144878169104055e-06, 0.04214000005801899, 0.0009694436354028095]
    star['Antares'] = [4.317104857204017, -0.461326764402159, -4.9257133320888044e-08,
                       -1.125252442724219e-07, 0.00540000000026852, 3.0393146561988747e-05]
    star['Arcturus'] = [3.733465394773943, 0.3346848334294686, -5.3007843606556596e-06,
                        -9.69346477902228e-06, 0.08885000153229092, 0.015051997164824159]
    star['Arided'] = [5.416768664385171, 0.7902910708184445, 7.563094744278182e-09,
                      7.514611728575477e-09, 0.0010100000000015834, 9.432289969961166e-07]
    star['Aridif'] = [5.416768664385171, 0.7902910708184445, 7.563094744278182e-09,
                      7.514611728575477e-09, 0.0010100000000015834, 9.432289969961166e-07]
    star['Aspidiske'] = [2.4307631077104497, -1.0345471855622463, -9.22598167724338e-08,
                         6.355911655058998e-08, 0.004710000000115389, 1.4937001081439416e-05]
    star['Atria'] = [4.401131946452735, -1.20476273657625, 8.654006996517539e-08,
                     -1.5960063467623645e-07, 0.0078499999999863, 0.0007217887018293024]
    star['Avior'] = [2.1926292266294993, -1.0386351499877453, -1.2285125864215074e-07,
                     1.1014974417412152e-07, 0.005160000000294713, 3.487935501970503e-05]
    star['Becrux'] = [3.3498123370879367, -1.041766165790106, -2.338746911835965e-07,
                      -6.215284007319667e-08, 0.009250000000322599, 2.161530508380125e-05]
    star['Bellatrix'] = [1.4186513478515415, 0.11082247066095403, -4.242119011236463e-08,
                         -6.438325912420494e-08, 0.013420000000105736, 4.958681667120478e-06]
    star['Benetnash'] = [3.6108204064416527, 0.8606779733601759, -5.877384404033237e-07,
                         -7.54389709946754e-08, 0.03239000000253164, 5.290086966817523e-05]
    star['Betelgeuse'] = [1.5497306535434074, 0.1292782376391354, 1.3249959988945085e-07,
                          5.2650739978285095e-08, 0.007630000000365368, 2.9504741916182075e-05]
    star['Birdun'] = [3.577433890408792, -0.9331653230878826, -7.07829335898563e-08,
                      -6.200764227622591e-08, 0.0086800000001021, 7.275220371534646e-06]
    star['Canopus'] = [1.6753070194885678, -0.9197114578906895, 9.691391940077004e-08,
                       1.1475545034562322e-07, 0.01043000000029997, 1.7902131155245466e-05]
    star['Capella'] = [1.3818220315092138, 0.8027925992180007, 3.66113248517538e-07,
                       -2.0707854322123023e-06, 0.07728999997778925, 0.0017946680558414705]
    star['Caph'] = [0.04007610542216626, 1.0323483546064598, 2.5373809290596606e-06,
                    -8.747334138705358e-07, 0.05989000003634503, 0.0004611720274889318]
    star['Castor'] = [1.983545223291272, 0.5565471590712135, -1.0003057907639829e-06,
                      -7.184020680791945e-07, 0.063269999994831, 0.0007126868274926918]
    star['Deneb'] = [5.416768664385171, 0.7902910708184445, 7.563094744278182e-09,
                     7.514611728575477e-09, 0.0010100000000015834, 9.432289969961166e-07]
    star['Deneb Kaitos'] = [0.1902081188358614, -0.31392364918918647, 1.1285964326896069e-06,
                            1.5858685374080113e-07, 0.034040000019417684, 0.00038863263469310187]
    star['Denebola'] = [3.093828467980623, 0.2543240927106615, -2.419309256680917e-06,
                        -5.516373829388986e-07, 0.09016000007399483, 0.000721149630524313]
    star['Diphda'] = [0.1902081188358614, -0.31392364918918647, 1.1285964326896069e-06,
                      1.5858685374080113e-07, 0.034040000019417684, 0.00038863263469310187]
    star['Dschubba'] = [4.190244618144675, -0.39482537631970344, -4.2033418163817215e-08,
                        -1.7889624112036493e-07, 0.008120000000609964, 4.636649173215924e-05]
    star['Dubhe'] = [2.8960513101567353, 1.077756882121675, -6.615719125458324e-07,
                     -1.7089891926750653e-07, 0.02637999999977838, 0.00034578378814995904]
    star['Durre Menthor'] = [0.45398660415481645, -0.2781139211407137, -8.347392014614402e-06,
                             4.140859553476101e-06, 0.27417000005208925, 0.0033429174261659328]
    star['Elnath'] = [1.423718247509374, 0.4992844876664838, 1.1286343012058481e-07,
                      -8.446424566762641e-07, 0.024890000012364286, 0.0003264766853078367]
    star['Enif'] = [5.690586474843174, 0.1723515371089685, 1.4554107096417846e-07,
                    6.690387674842033e-09, 0.004850000000379499, 4.773139317546102e-05]
    star['Etamin'] = [4.697580104940832, 0.8986494616265581, -4.1305992314530515e-08,
                      -1.1174956302938611e-07, 0.022099999999980816, 4.9615702010916675e-05]
    star['Fomalhaut'] = [6.011153831667956, -0.5170147010899686, 1.5961202056558495e-06,
                         -7.961484485636487e-07, 0.13008000002597714, 0.00022103393638362462]
    star['Foramen'] = [4.97547985577903, -0.9602020060794809, 8.193327273465503e-09,
                       8.896331084586689e-08, 0.004790000000146212, 1.8616196638782124e-05]
    star['Gacrux'] = [3.277581487979869, -0.9968283158561463, 1.354631124161606e-07,
                      -1.2815079068589154e-06, 0.037090000026841055, 0.0004991250501088714]
    star['Gemma'] = [4.078351611721369, 0.46625436926948094, 5.836157823581908e-07,
                     -4.3361892800692933e-07, 0.043650000007291134, 0.00011835310422146781]
    star['Gienah'] = [5.437642775929634, 0.5929112160847636, 1.726755217907226e-06,
                      1.6012267484412231e-06, 0.045260000072684665, 0.0011455600319130637]
    star['Girtab'] = [4.613424102927273, -0.7504536504558865, 2.9379711974897553e-08,
                      -4.605725023422437e-09, 0.011990000000008667, 4.5254804610896223e-07]
    star['Gruid'] = [5.945766228928144, -0.8182904865556216, 6.577955533321446e-07,
                     -2.186261632616384e-08, 0.01916999999974359, 0.0009978597297020174]
    star['Hadar'] = [3.6818723020537076, -1.053709711449934, -1.6464353444471552e-07,
                     -1.2149417463462386e-07, 0.006210000000391972, 3.869200910092055e-05]
    star['Hamal'] = [0.5549094887514628, 0.4094884133752071, 9.246786155531776e-07,
                     -7.067164911970393e-07, 0.04948000001885987, 0.00027678915662970914]
    star['Herschel Star'] = [5.687625505342922, 1.0259051781286534, 2.54042234405336e-08,
                             -1.3962637303125504e-08, 0.0006200000000068873, 6.675057144558865e-06]
    star['Izar'] = [3.861481258187226, 0.4725354381874391, -2.455584091808065e-07,
                    9.696245541856035e-08, 0.015550000001013312, 4.133628709474172e-05]
    star['Kaus Australis'] = [4.817856898473025, -0.6001316738325381, -1.920365154066435e-07,
                              -6.014111738890365e-07, 0.022550000006672573, 0.00019272943416765549]
    star['Kochab'] = [3.886433850504668, 1.2942583826097445, -1.5654706957982152e-07,
                      5.77412354561257e-08, 0.02579000000008792, 2.2483739731882224e-06]
    star['Koo She'] = [2.2894537118978118, -0.954854859381276, 1.3953166459127527e-07,
                       -5.048848614565181e-07, 0.040899999999294154, 0.00032099051055673215]
    star['Marchab'] = [6.0421626524685905, 0.26537955671991786, 2.96220777378518e-07,
                       -2.0633695786708617e-07, 0.02336000000213731, 5.977832383281093e-05]
    star['Marfikent'] = [3.8201182532289284, -0.7357946496215423, -1.711882706511818e-07,
                         -1.572733902801985e-07, 0.010569999999971503, 0.0006262735012201731]
    star['Markab'] = [2.4526828441605657, -0.9601166539897806, -5.1971933625336406e-08,
                      5.449307233758287e-08, 0.006050000000070748, 7.164123670877446e-06]
    star['Megrez'] = [3.2089070543303073, 0.9954073810426787, 5.02073721730927e-07,
                      3.786262609458028e-08, 0.04005000000122444, 2.13424718460294e-05]
    star['Men'] = [3.848141162334873, -0.8270814682688525, -1.0253839404380364e-07,
                   -1.1742181302475734e-07, 0.00594999999999269, 0.0008732238462943129]
    star['Menkalinan'] = [1.5687368179332424, 0.7844806433201716, -2.734833707459999e-07,
                          -4.266790108143737e-09, 0.039720000000604105, 1.060291154252638e-05]
    star['Menkent'] = [3.694320294230699, -0.6348043036838847, -2.5176959465502842e-06,
                       -2.5106698293240554e-06, 0.05352000015833705, 0.0021860406901616784]
    star['Merak'] = [2.887831914491518, 0.9840608672971128, 3.95901090538103e-07,
                     1.635753056423083e-07, 0.04107000000119887, 2.046330757267866e-05]
    star['Miaplacidus'] = [2.413779789942438, -1.2167887530125798, -7.643321532299717e-07,
                           5.280127629333715e-07, 0.029340000005863925, 0.00013364856100836408]
    star['Mimosa'] = [3.3498123370879367, -1.041766165790106, -2.338746911835965e-07,
                      -6.215284007319667e-08, 0.009250000000322599, 2.161530508380125e-05]
    star['Mintaka'] = [1.4486525135863997, -0.005220109648199803, 8.096388471892125e-09,
                       2.7149566181452945e-09, 0.0035600000000013494, 2.3014217356530194e-07]
    star['Mira'] = [0.6080145769855249, -0.051983008794519885, 5.008132276737923e-08,
                    -1.1610318018188046e-06, 0.007790000024612303, 0.0019478308211168475]
    star['Mirach'] = [0.30427329086861893, 0.621689761001418, 8.512767159283747e-07,
                      -5.441103366318654e-07, 0.016360000013684175, 0.0005321917632525456]
    star['Mirfak'] = [0.8915279133021705, 0.8702403038092067, 1.1688817634374709e-07,
                      -1.261001153321045e-07, 0.0055099999999921505, 0.0011773710216326351]
    star['Mirzam'] = [1.6698424995060674, -0.313389910655518, -1.672607228212473e-08,
                      -2.2786233584483583e-09, 0.006530000000004731, 4.4454535471340125e-07]
    star['Mizar'] = [3.5077944215549155, 0.9586271792673523, 5.877375728743625e-07,
                     -1.0670935794835243e-07, 0.04173000000200527, 3.3778110250685826e-05]
    star['Muhlifein'] = [3.322735659757405, -0.8545113215907899, -9.07959201334906e-07,
                         -5.813072916876795e-09, 0.02501000000607358, 0.00015967627031789804]
    star['Murzim'] = [1.6698424995060674, -0.313389910655518, -1.672607228212473e-08,
                      -2.2786233584483583e-09, 0.006530000000004731, 4.4454535471340125e-07]
    star['Naos'] = [2.1100320210600567, -0.6981857042817188, -1.4941934222649785e-07,
                    8.130338064789374e-08, 0.002330000000366323, 9.504703265245339e-05]
    star['Nunki'] = [4.953530676197697, -0.4589673187899529, 6.72438524966264e-08,
                     -2.552543824655031e-07, 0.014540000001223, 5.315575428825297e-05]
    star['Peacock'] = [5.347897085056093, -0.9902189230127056, 3.73796816285248e-08,
                       -4.176669775229641e-07, 0.017799999999794508, 0.000990428953167536]
    star['Phad'] = [3.1146804039583205, 0.9371509762387942, 5.224361069083074e-07,
                    5.41037103447854e-08, 0.03899000000159402, 2.8416177345077626e-05]
    star['Phecda'] = [3.1146804039583205, 0.9371509762387942, 5.224361069083074e-07,
                      5.41037103447854e-08, 0.03899000000159402, 2.8416177345077626e-05]
    star['Polaris'] = [0.6624337222159393, 1.5579519607443513, 2.1436277908348448e-07,
                       -5.691713294404453e-08, 0.007560000000059228, 4.825858861368139e-06]
    star['Pollux'] = [2.0302885080344946, 0.4891468825834284, -3.0334224510739657e-06,
                      -2.2281574203528431e-07, 0.09674000008918031, 0.0008385163461058639]
    star['Procyon'] = [2.0040429992164794, 0.09113569709349426, -3.4739927692981882e-06,
                       -5.015797930119599e-06, 0.28592999999488294, 0.0014588955840861995]
    star['Ras Alhague'] = [4.603026277462708, 0.21920155963486707, 5.336799510847808e-07,
                           -1.079244429963408e-06, 0.06984000002028967, 0.00023103642537959567]
    star['Rasalhague'] = [4.603026277462708, 0.21920155963486707, 5.336799510847808e-07,
                          -1.079244429963408e-06, 0.06984000002028967, 0.00023103642537959567]
    star['Regor'] = [2.135988167263121, -0.8261787606380119, -2.874941688021273e-08,
                     4.7996559162769396e-08, 0.003880000000049594, 7.77011047797864e-06]
    star['Regulus'] = [2.6545090465732897, 0.20886743903385466, -1.209125460656726e-06,
                       2.3800944074611064e-08, 0.042090000022339376, 0.00037363640989622346]
    star['Rigel'] = [1.3724304784606873, -0.14314566287888414, 9.066015918278104e-09,
                     -2.714956480857884e-09, 0.004220000000001623, 2.3400594582481953e-07]
    star['Rigel Kent'] = [3.8378101832191707, -1.0617263036155733, -1.78306523693292e-05,
                          2.337581054645688e-06, 0.7421199975499211, 0.001226041150778626]
    star['Rigil Kentaurus'] = [3.8378101832191707, -1.0617263036155733, -1.78306523693292e-05,
                               2.337581054645688e-06, 0.7421199975499211, 0.001226041150778626]
    star['Sabik'] = [4.4958749856971805, -0.27444601806556124, 1.9954869986299388e-07,
                     4.7342067895237334e-07, 0.03877000000422318, 7.564441169146644e-05]
    star['Sadira'] = [0.9290312107794707, -0.16507681479027084, -4.733913114822857e-06,
                      8.716275879308175e-08, 0.3107499999612522, 0.0007886552931391373]
    star['Sadr'] = [5.332977429615501, 0.7026115468408063, 1.178097141729761e-08,
                    -4.508768020822042e-09, 0.0021400000000018813, 5.311291070290127e-07]
    star['Saiph'] = [1.5173739831782236, -0.16876650756993367, 7.514612228387732e-09,
                     -5.817764065873347e-09, 0.004520000000001636, 2.2054196512592592e-07]
    star['Sargas'] = [4.613424102927273, -0.7504536504558865, 2.9379711974897553e-08,
                      -4.605725023422437e-09, 0.011990000000008667, 4.5254804610896223e-07]
    star['Scheat'] = [6.037864835040629, 0.4901447987867555, 9.102936143737786e-07,
                      6.671481519153598e-07, 0.016370000019248994, 0.0007481838158161249]
    star['Schedar'] = [0.17674942738602892, 0.9867607856371221, 2.441508454838371e-07,
                       -1.5596487610355452e-07, 0.014269999999960009, 0.0003658193236540751]
    star['Scutulum'] = [2.4307631077104497, -1.0345471855622463, -9.22598167724338e-08,
                        6.355911655058998e-08, 0.004710000000115389, 1.4937001081439416e-05]
    star['Shaula'] = [4.597234568366436, -0.6475855125314752, -4.314852652855297e-08,
                      -1.4520168719893398e-07, 0.004640000000410453, 5.392052018593021e-05]
    star['Sirius'] = [1.767763933302459, -0.2918193953521118, -2.6472395013586827e-06,
                      -5.929636920612978e-06, 0.3792099989588343, 0.0016933838990403176]
    star['Sirrah'] = [0.036605554597617405, 0.5077147413037055, 6.577885543330571e-07,
                      -7.90006001232231e-07, 0.03359999999788266, 0.0016673676990050404]
    star['South Star'] = [5.5361018859074305, -1.5525835188814383, 1.2585376697957656e-07,
                          2.4337650105845932e-08, 0.012070000000010723, 5.56262997395674e-07]
    star['Spica'] = [3.513314821192477, -0.19480358596412684, -2.060459576954052e-07,
                     -1.5383128799730128e-07, 0.012439999999947002, 0.0007231726564263089]
    star['Suhail'] = [2.3910822168119714, -0.7580408913310245, -1.1252508588992842e-07,
                      6.923146630098186e-08, 0.005690000000210632, 2.264919342445772e-05]
    star['Thuban'] = [3.6843396163473385, 1.1235715078189106, -2.740177867539633e-07,
                      8.333913535295936e-08, 0.010560000000378668, 2.2331125543834043e-05]
    star['Toliman'] = [3.8378101832191707, -1.0617263036155733, -1.78306523693292e-05,
                       2.337581054645688e-06, 0.7421199975499211, 0.001226041150778626]
    star['Tseen She'] = [4.97547985577903, -0.9602020060794809, 8.193327273465503e-09,
                         8.896331084586689e-08, 0.004790000000146212, 1.8616196638782124e-05]
    star['Tsih'] = [0.2474405188510991, 1.059706817818162, 1.2435461482456956e-07,
                    -1.8519958426771e-08, 0.0053200000000743364, 8.537994463884992e-06]
    star['Turais'] = [2.4307631077104497, -1.0345471855622463, -9.22598167724338e-08,
                      6.355911655058998e-08, 0.004710000000115389, 1.4937001081439416e-05]
    star['Vega'] = [4.873576712264601, 0.6769191319297997, 9.745975424585287e-07,
                    1.3936400760062212e-06, 0.12892999997855553, 0.000461224580198702]
    star['Wei'] = [4.407635896267798, -0.5985440584766897, -2.966293212623124e-06,
                   -1.24044570196882e-06, 0.04985000011654288, 0.001700383320118473]
    star['Wezen'] = [1.8692099697512634, -0.4606480488021012, -1.3332373766994271e-08,
                     1.6144296383671154e-08, 0.0018199999999999514, 0.00019661873306528355]

    return star

