function Effect_CaptionRatio10003(level){
function SCR_REINFORCEABILITY_TOOLTIP(skill) {
    var addAbilRate = 1;

    if ("Swordman13" != "None") {
        var reinforceAbil = GetAbility(pc, "Swordman13")

        if (reinforceAbil != null) {
            var abilLevel = TryGetProp(reinforceAbil, "Level")
            var masterAddValue = 0

            if (abilLevel == 100) {
                masterAddValue = 0.1
            }

            addAbilRate = 1 + (reinforceAbil.Level * 0.005 + masterAddValue);
            var hidden_abil_cls = GetClass("HiddenAbility_Reinforce", skill.ClassName);

            if (abilLevel >= 65  &&  hidden_abil_cls != null) {
                var hidden_abil_name = TryGetProp(hidden_abil_cls, "HiddenReinforceAbil");
                var hidden_abil = GetAbility(pc, hidden_abil_name);

                if (hidden_abil != null) {
                    var abil_level = TryGetProp(hidden_abil, "Level");
                    var add_factor = TryGetProp(hidden_abil_cls, "FactorByLevel", 0) * 0.01;
                    var add_value = 0;

                    if (abil_level == 10) {
                        add_value = TryGetProp(hidden_abil_cls, "AddFactor", 0) * 0.01
                    }

                    addAbilRate = addAbilRate * (1 + (abil_level * add_factor) + add_value);
                }

            }

        }

    }

    return addAbilRate
}

var value = skill.Level * 2;
value = value * SCR_REINFORCEABILITY_TOOLTIP(skill)
return value;
}
function Effect_CaptionRatio10004(level){
return skill.Level * 2;
}
function Effect_CaptionRatio10006(level){
var value = skill.Level * 6
return Math.floor(value);
}
function Effect_CaptionRatio10007(level){
return (1 + (skill.Level - 1) * 0.5)
}
function Effect_CaptionRatio10009(level){
function SCR_REINFORCEABILITY_TOOLTIP(skill) {
    var addAbilRate = 1;

    if ("Swordman30" != "None") {
        var reinforceAbil = GetAbility(pc, "Swordman30")

        if (reinforceAbil != null) {
            var abilLevel = TryGetProp(reinforceAbil, "Level")
            var masterAddValue = 0

            if (abilLevel == 100) {
                masterAddValue = 0.1
            }

            addAbilRate = 1 + (reinforceAbil.Level * 0.005 + masterAddValue);
            var hidden_abil_cls = GetClass("HiddenAbility_Reinforce", skill.ClassName);

            if (abilLevel >= 65  &&  hidden_abil_cls != null) {
                var hidden_abil_name = TryGetProp(hidden_abil_cls, "HiddenReinforceAbil");
                var hidden_abil = GetAbility(pc, hidden_abil_name);

                if (hidden_abil != null) {
                    var abil_level = TryGetProp(hidden_abil, "Level");
                    var add_factor = TryGetProp(hidden_abil_cls, "FactorByLevel", 0) * 0.01;
                    var add_value = 0;

                    if (abil_level == 10) {
                        add_value = TryGetProp(hidden_abil_cls, "AddFactor", 0) * 0.01
                    }

                    addAbilRate = addAbilRate * (1 + (abil_level * add_factor) + add_value);
                }

            }

        }

    }

    return addAbilRate
}

var value = skill.Level * 2;
value = value * SCR_REINFORCEABILITY_TOOLTIP(skill)
return value;
}
function Effect_CaptionRatio10102(){
var value = 0
var abil = GetAbility(pc, "Peltasta38")

if (abil != null  &&  TryGetProp(abil, "ActiveState", 0) == 1) {
    value = value + TryGetProp(abil, "Level", 0) * 3
}

return value
}
function Effect_CaptionRatio10103(level){
var value = 4 * skill.Level;

if (IsPVPField(pc) == 1  &&  value > 2) {
    value = Math.floor((Math.pow(Math.max(0, value-2), 0.5)))+Math.min(2, value)
}

return value
}
function Effect_CaptionRatio10104(level){
function SCR_REINFORCEABILITY_TOOLTIP(skill) {
    var addAbilRate = 1;

    if ("Peltasta13" != "None") {
        var reinforceAbil = GetAbility(pc, "Peltasta13")

        if (reinforceAbil != null) {
            var abilLevel = TryGetProp(reinforceAbil, "Level")
            var masterAddValue = 0

            if (abilLevel == 100) {
                masterAddValue = 0.1
            }

            addAbilRate = 1 + (reinforceAbil.Level * 0.005 + masterAddValue);
            var hidden_abil_cls = GetClass("HiddenAbility_Reinforce", skill.ClassName);

            if (abilLevel >= 65  &&  hidden_abil_cls != null) {
                var hidden_abil_name = TryGetProp(hidden_abil_cls, "HiddenReinforceAbil");
                var hidden_abil = GetAbility(pc, hidden_abil_name);

                if (hidden_abil != null) {
                    var abil_level = TryGetProp(hidden_abil, "Level");
                    var add_factor = TryGetProp(hidden_abil_cls, "FactorByLevel", 0) * 0.01;
                    var add_value = 0;

                    if (abil_level == 10) {
                        add_value = TryGetProp(hidden_abil_cls, "AddFactor", 0) * 0.01
                    }

                    addAbilRate = addAbilRate * (1 + (abil_level * add_factor) + add_value);
                }

            }

        }

    }

    return addAbilRate
}

var value = 8 * skill.Level

if (IsPVPField(pc) == 1) {
    value = 5 * skill.Level
}

value = Math.floor(value * SCR_REINFORCEABILITY_TOOLTIP(skill))
return value;
}
function Effect_CaptionRatio10105(){
var value = 0
var abil = GetAbility(pc, "Peltasta38")

if (abil != null  &&  TryGetProp(abil, "ActiveState", 0) == 1) {
    value = value + TryGetProp(abil, "Level", 0) * 3
}

return value
}
function Effect_CaptionRatio10106(){
function SCR_REINFORCEABILITY_TOOLTIP(skill) {
    var addAbilRate = 1;

    if ("Peltasta36" != "None") {
        var reinforceAbil = GetAbility(pc, "Peltasta36")

        if (reinforceAbil != null) {
            var abilLevel = TryGetProp(reinforceAbil, "Level")
            var masterAddValue = 0

            if (abilLevel == 100) {
                masterAddValue = 0.1
            }

            addAbilRate = 1 + (reinforceAbil.Level * 0.005 + masterAddValue);
            var hidden_abil_cls = GetClass("HiddenAbility_Reinforce", skill.ClassName);

            if (abilLevel >= 65  &&  hidden_abil_cls != null) {
                var hidden_abil_name = TryGetProp(hidden_abil_cls, "HiddenReinforceAbil");
                var hidden_abil = GetAbility(pc, hidden_abil_name);

                if (hidden_abil != null) {
                    var abil_level = TryGetProp(hidden_abil, "Level");
                    var add_factor = TryGetProp(hidden_abil_cls, "FactorByLevel", 0) * 0.01;
                    var add_value = 0;

                    if (abil_level == 10) {
                        add_value = TryGetProp(hidden_abil_cls, "AddFactor", 0) * 0.01
                    }

                    addAbilRate = addAbilRate * (1 + (abil_level * add_factor) + add_value);
                }

            }

        }

    }

    return addAbilRate
}

var value = 50
value = Math.floor(value * SCR_REINFORCEABILITY_TOOLTIP(skill));
return value
}
function Effect_CaptionRatio10109(){
var value = 30
var abil = GetAbility(pc, "Peltasta38")

if (abil != null  &&  TryGetProp(abil, "ActiveState", 0) == 1) {
    value = value + TryGetProp(abil, "Level", 0) * 3
}

return value
}
function Effect_CaptionRatio10110(level){
function SCR_REINFORCEABILITY_TOOLTIP(skill) {
    var addAbilRate = 1;

    if ("Peltasta37" != "None") {
        var reinforceAbil = GetAbility(pc, "Peltasta37")

        if (reinforceAbil != null) {
            var abilLevel = TryGetProp(reinforceAbil, "Level")
            var masterAddValue = 0

            if (abilLevel == 100) {
                masterAddValue = 0.1
            }

            addAbilRate = 1 + (reinforceAbil.Level * 0.005 + masterAddValue);
            var hidden_abil_cls = GetClass("HiddenAbility_Reinforce", skill.ClassName);

            if (abilLevel >= 65  &&  hidden_abil_cls != null) {
                var hidden_abil_name = TryGetProp(hidden_abil_cls, "HiddenReinforceAbil");
                var hidden_abil = GetAbility(pc, hidden_abil_name);

                if (hidden_abil != null) {
                    var abil_level = TryGetProp(hidden_abil, "Level");
                    var add_factor = TryGetProp(hidden_abil_cls, "FactorByLevel", 0) * 0.01;
                    var add_value = 0;

                    if (abil_level == 10) {
                        add_value = TryGetProp(hidden_abil_cls, "AddFactor", 0) * 0.01
                    }

                    addAbilRate = addAbilRate * (1 + (abil_level * add_factor) + add_value);
                }

            }

        }

    }

    return addAbilRate
}

var value = 20 * skill.Level
value = Math.floor(value * SCR_REINFORCEABILITY_TOOLTIP(skill));
return Math.floor(value)
}
function Effect_CaptionRatio10204(level){
var value = 95 + skill.Level * 5
return value
}
function Effect_CaptionRatio10303(level){
function SCR_REINFORCEABILITY_TOOLTIP(skill) {
    var addAbilRate = 1;

    if ("Hoplite32" != "None") {
        var reinforceAbil = GetAbility(pc, "Hoplite32")

        if (reinforceAbil != null) {
            var abilLevel = TryGetProp(reinforceAbil, "Level")
            var masterAddValue = 0

            if (abilLevel == 100) {
                masterAddValue = 0.1
            }

            addAbilRate = 1 + (reinforceAbil.Level * 0.005 + masterAddValue);
            var hidden_abil_cls = GetClass("HiddenAbility_Reinforce", skill.ClassName);

            if (abilLevel >= 65  &&  hidden_abil_cls != null) {
                var hidden_abil_name = TryGetProp(hidden_abil_cls, "HiddenReinforceAbil");
                var hidden_abil = GetAbility(pc, hidden_abil_name);

                if (hidden_abil != null) {
                    var abil_level = TryGetProp(hidden_abil, "Level");
                    var add_factor = TryGetProp(hidden_abil_cls, "FactorByLevel", 0) * 0.01;
                    var add_value = 0;

                    if (abil_level == 10) {
                        add_value = TryGetProp(hidden_abil_cls, "AddFactor", 0) * 0.01
                    }

                    addAbilRate = addAbilRate * (1 + (abil_level * add_factor) + add_value);
                }

            }

        }

    }

    return addAbilRate
}

var value = 3 * skill.Level + 15
value = value * SCR_REINFORCEABILITY_TOOLTIP(skill);
return value
}
function Effect_CaptionRatio10308(level){
function SCR_REINFORCEABILITY_TOOLTIP(skill) {
    var addAbilRate = 1;

    if ("Hoplite31" != "None") {
        var reinforceAbil = GetAbility(pc, "Hoplite31")

        if (reinforceAbil != null) {
            var abilLevel = TryGetProp(reinforceAbil, "Level")
            var masterAddValue = 0

            if (abilLevel == 100) {
                masterAddValue = 0.1
            }

            addAbilRate = 1 + (reinforceAbil.Level * 0.005 + masterAddValue);
            var hidden_abil_cls = GetClass("HiddenAbility_Reinforce", skill.ClassName);

            if (abilLevel >= 65  &&  hidden_abil_cls != null) {
                var hidden_abil_name = TryGetProp(hidden_abil_cls, "HiddenReinforceAbil");
                var hidden_abil = GetAbility(pc, hidden_abil_name);

                if (hidden_abil != null) {
                    var abil_level = TryGetProp(hidden_abil, "Level");
                    var add_factor = TryGetProp(hidden_abil_cls, "FactorByLevel", 0) * 0.01;
                    var add_value = 0;

                    if (abil_level == 10) {
                        add_value = TryGetProp(hidden_abil_cls, "AddFactor", 0) * 0.01
                    }

                    addAbilRate = addAbilRate * (1 + (abil_level * add_factor) + add_value);
                }

            }

        }

    }

    return addAbilRate
}

var value = 10 + (skill.Level * 2)
value = value * SCR_REINFORCEABILITY_TOOLTIP(skill)
return value
}
function Effect_CaptionRatio10402(level){
return Math.floor(10 + skill.Level * 5)
}
function Effect_CaptionRatio10405(){
function SCR_REINFORCEABILITY_TOOLTIP(skill) {
    var addAbilRate = 1;

    if ("Barbarian11" != "None") {
        var reinforceAbil = GetAbility(pc, "Barbarian11")

        if (reinforceAbil != null) {
            var abilLevel = TryGetProp(reinforceAbil, "Level")
            var masterAddValue = 0

            if (abilLevel == 100) {
                masterAddValue = 0.1
            }

            addAbilRate = 1 + (reinforceAbil.Level * 0.005 + masterAddValue);
            var hidden_abil_cls = GetClass("HiddenAbility_Reinforce", skill.ClassName);

            if (abilLevel >= 65  &&  hidden_abil_cls != null) {
                var hidden_abil_name = TryGetProp(hidden_abil_cls, "HiddenReinforceAbil");
                var hidden_abil = GetAbility(pc, hidden_abil_name);

                if (hidden_abil != null) {
                    var abil_level = TryGetProp(hidden_abil, "Level");
                    var add_factor = TryGetProp(hidden_abil_cls, "FactorByLevel", 0) * 0.01;
                    var add_value = 0;

                    if (abil_level == 10) {
                        add_value = TryGetProp(hidden_abil_cls, "AddFactor", 0) * 0.01
                    }

                    addAbilRate = addAbilRate * (1 + (abil_level * add_factor) + add_value);
                }

            }

        }

    }

    return addAbilRate
}

var value = SCR_REINFORCEABILITY_TOOLTIP(skill)
return value;
}
function Effect_CaptionRatio10406(level){
var value = 150 + (skill.Level * 10)
return Math.floor(value)
}
function Effect_CaptionRatio10501(level){
var value = 10 + (skill.Level * 6)
return value;
}
function Effect_CaptionRatio10503(){
var value = 0
var abil = GetAbility(pc, "Rodelero31")

if (abil != null  &&  TryGetProp(abil, "ActiveState", 0) == 1) {
    value = abil.Level * 3
}

return value
}
function Effect_CaptionRatio10504(level){
var value = skill.Level
return value;
}
function Effect_CaptionRatio10505(level){
var value = skill.Level * 10
return value
}
function Effect_CaptionRatio10506(){
var value = 0
var abil = GetAbility(pc, "Rodelero31")

if (abil != null  &&  TryGetProp(abil, "ActiveState", 0) == 1) {
    value = abil.Level * 3
}

return value
}
function Effect_CaptionRatio10507(){
var value = 0
var abil = GetAbility(pc, "Rodelero31")

if (abil != null  &&  TryGetProp(abil, "ActiveState", 0) == 1) {
    value = abil.Level * 3
}

return value
}
function Effect_CaptionRatio10508(){
var value = 0
var abil = GetAbility(pc, "Rodelero31")

if (abil != null  &&  TryGetProp(abil, "ActiveState", 0) == 1) {
    value = abil.Level * 3
}

return value
}
function Effect_CaptionRatio10603(level){
var value = skill.Level + 5
return value
}
function Effect_CaptionRatio10605(){
var value = 10 + TryGetProp(skill, "Level", 1)
return value
}
function Effect_CaptionRatio10608(level){
function SCR_REINFORCEABILITY_TOOLTIP(skill) {
    var addAbilRate = 1;

    if ("Cataphract33" != "None") {
        var reinforceAbil = GetAbility(pc, "Cataphract33")

        if (reinforceAbil != null) {
            var abilLevel = TryGetProp(reinforceAbil, "Level")
            var masterAddValue = 0

            if (abilLevel == 100) {
                masterAddValue = 0.1
            }

            addAbilRate = 1 + (reinforceAbil.Level * 0.005 + masterAddValue);
            var hidden_abil_cls = GetClass("HiddenAbility_Reinforce", skill.ClassName);

            if (abilLevel >= 65  &&  hidden_abil_cls != null) {
                var hidden_abil_name = TryGetProp(hidden_abil_cls, "HiddenReinforceAbil");
                var hidden_abil = GetAbility(pc, hidden_abil_name);

                if (hidden_abil != null) {
                    var abil_level = TryGetProp(hidden_abil, "Level");
                    var add_factor = TryGetProp(hidden_abil_cls, "FactorByLevel", 0) * 0.01;
                    var add_value = 0;

                    if (abil_level == 10) {
                        add_value = TryGetProp(hidden_abil_cls, "AddFactor", 0) * 0.01
                    }

                    addAbilRate = addAbilRate * (1 + (abil_level * add_factor) + add_value);
                }

            }

        }

    }

    return addAbilRate
}

var value = 20 + (skill.Level * 4)
value = value * SCR_REINFORCEABILITY_TOOLTIP(skill);
return value;
}
function Effect_CaptionRatio10901(level){
var value = 3 + skill.Level;

if (value > 8) {
    value = 8
}

return value
}
function Effect_CaptionRatio10902(level){
return skill.Level * 10
}
function Effect_CaptionRatio10903(level){
return skill.Level * 10
}
function Effect_CaptionRatio10904(level){
var value = 50 + (3 * skill.Level)
return value;
}
function Effect_CaptionRatio10905(){
return 4
}
function Effect_CaptionRatio10907(){
return 50
}
function Effect_CaptionRatio10910(level){
var value = 35 + skill.Level * 5
return value;
}
function Effect_CaptionRatio11003(level){
var value = skill.Level * 30
return value
}
function Effect_CaptionRatio11110(level){
function SCR_REINFORCEABILITY_TOOLTIP(skill) {
    var addAbilRate = 1;

    if ("Fencer12" != "None") {
        var reinforceAbil = GetAbility(pc, "Fencer12")

        if (reinforceAbil != null) {
            var abilLevel = TryGetProp(reinforceAbil, "Level")
            var masterAddValue = 0

            if (abilLevel == 100) {
                masterAddValue = 0.1
            }

            addAbilRate = 1 + (reinforceAbil.Level * 0.005 + masterAddValue);
            var hidden_abil_cls = GetClass("HiddenAbility_Reinforce", skill.ClassName);

            if (abilLevel >= 65  &&  hidden_abil_cls != null) {
                var hidden_abil_name = TryGetProp(hidden_abil_cls, "HiddenReinforceAbil");
                var hidden_abil = GetAbility(pc, hidden_abil_name);

                if (hidden_abil != null) {
                    var abil_level = TryGetProp(hidden_abil, "Level");
                    var add_factor = TryGetProp(hidden_abil_cls, "FactorByLevel", 0) * 0.01;
                    var add_value = 0;

                    if (abil_level == 10) {
                        add_value = TryGetProp(hidden_abil_cls, "AddFactor", 0) * 0.01
                    }

                    addAbilRate = addAbilRate * (1 + (abil_level * add_factor) + add_value);
                }

            }

        }

    }

    return addAbilRate
}

var value = 10 + skill.Level * 2;
value = value * SCR_REINFORCEABILITY_TOOLTIP(skill)
return Math.floor(value)
}
function Effect_CaptionRatio11302(){
var value = 0
var abil = GetAbility(pc, "Murmillo20")

if (abil != null  &&  TryGetProp(abil, "ActiveState", 0) == 1) {
    value = TryGetProp(abil, "Level", 0) * 3
}

return value
}
function Effect_CaptionRatio11307(){
var value = 0
var abil = GetAbility(pc, "Murmillo20")

if (abil != null  &&  TryGetProp(abil, "ActiveState", 0) == 1) {
    value = TryGetProp(abil, "Level", 0) * 3
}

return value
}
function Effect_CaptionRatio11308(){
var value = 10

if (IsPVPField(self) == 1  &&  value > 2) {
    value = Math.floor((Math.pow(Math.max(0, value-2), 0.5)))+Math.min(2, value)
}

return value
}
function Effect_CaptionRatio11309(level){
var value = skill.Level * 4
return value
}
function Effect_CaptionRatio11310(){
var value = 8
return value;
}
function Effect_CaptionRatio11311(){
var abil = GetAbility(pc, "Murmillo20")
var value = 30

if (abil != null  &&  TryGetProp(abil, "ActiveState", 0) == 1) {
    value = value + (TryGetProp(abil, "Level", 0) * 3)
}

return value
}
function Effect_CaptionRatio11407(){
var value = 30

if (IsPVPField(pc) == 1  &&  value > 2) {
    value = Math.floor((Math.pow(Math.max(0, value-2), 0.5)))+Math.min(2, value)
}

return value
}
function Effect_CaptionRatio11408(){
var value = 50
var abil = GetAbility(pc, "Dragoon20")

if (abil != null  &&  abil.ActiveState == 1) {
    value = 25
}

return value;
}
function Effect_CaptionRatio11409(level){
var value = 10 + (skill.Level-1) * 5
return value
}
function Effect_CaptionRatio11501(level){
var value = 1 * skill.Level
return value
}
function Effect_CaptionRatio11504(level){
var value = 5 * skill.Level
return value
}
function Effect_CaptionRatio11505(level){
var value = SCR_GET_BattleOrders_Ratio2(skill)
var addvalue = skill.Level * 1.5
value = value + addvalue
return value
}
function Effect_CaptionRatio11507(level){
var value = 5 + (skill.Level * 2)
return value
}
function Effect_CaptionRatio11509(level){
function SCR_REINFORCEABILITY_TOOLTIP(skill) {
    var addAbilRate = 1;

    if ("Templar5" != "None") {
        var reinforceAbil = GetAbility(pc, "Templar5")

        if (reinforceAbil != null) {
            var abilLevel = TryGetProp(reinforceAbil, "Level")
            var masterAddValue = 0

            if (abilLevel == 100) {
                masterAddValue = 0.1
            }

            addAbilRate = 1 + (reinforceAbil.Level * 0.005 + masterAddValue);
            var hidden_abil_cls = GetClass("HiddenAbility_Reinforce", skill.ClassName);

            if (abilLevel >= 65  &&  hidden_abil_cls != null) {
                var hidden_abil_name = TryGetProp(hidden_abil_cls, "HiddenReinforceAbil");
                var hidden_abil = GetAbility(pc, hidden_abil_name);

                if (hidden_abil != null) {
                    var abil_level = TryGetProp(hidden_abil, "Level");
                    var add_factor = TryGetProp(hidden_abil_cls, "FactorByLevel", 0) * 0.01;
                    var add_value = 0;

                    if (abil_level == 10) {
                        add_value = TryGetProp(hidden_abil_cls, "AddFactor", 0) * 0.01
                    }

                    addAbilRate = addAbilRate * (1 + (abil_level * add_factor) + add_value);
                }

            }

        }

    }

    return addAbilRate
}

var value = 10 + (skill.Level * 2)
value = value * SCR_REINFORCEABILITY_TOOLTIP(skill)
return value
}
function Effect_CaptionRatio11510(level){
var value = 5 + (skill.Level * 2)
return value
}
function Effect_CaptionRatio11513(level){
function SCR_REINFORCEABILITY_TOOLTIP(skill) {
    var addAbilRate = 1;

    if ("Templar7" != "None") {
        var reinforceAbil = GetAbility(pc, "Templar7")

        if (reinforceAbil != null) {
            var abilLevel = TryGetProp(reinforceAbil, "Level")
            var masterAddValue = 0

            if (abilLevel == 100) {
                masterAddValue = 0.1
            }

            addAbilRate = 1 + (reinforceAbil.Level * 0.005 + masterAddValue);
            var hidden_abil_cls = GetClass("HiddenAbility_Reinforce", skill.ClassName);

            if (abilLevel >= 65  &&  hidden_abil_cls != null) {
                var hidden_abil_name = TryGetProp(hidden_abil_cls, "HiddenReinforceAbil");
                var hidden_abil = GetAbility(pc, hidden_abil_name);

                if (hidden_abil != null) {
                    var abil_level = TryGetProp(hidden_abil, "Level");
                    var add_factor = TryGetProp(hidden_abil_cls, "FactorByLevel", 0) * 0.01;
                    var add_value = 0;

                    if (abil_level == 10) {
                        add_value = TryGetProp(hidden_abil_cls, "AddFactor", 0) * 0.01
                    }

                    addAbilRate = addAbilRate * (1 + (abil_level * add_factor) + add_value);
                }

            }

        }

    }

    return addAbilRate
}

var value = skill.Level * 8
value = value * SCR_REINFORCEABILITY_TOOLTIP(skill)
return value
}
function Effect_CaptionRatio11601(level){
var value = skill.Level
return value
}
function Effect_CaptionRatio11606(level){
var value = skill.Level * 10
return value
}
function Effect_CaptionRatio11607(level){
var value = skill.Level * 3
return value
}
function Effect_CaptionRatio11701(level){
var value = 10 + skill.Level * 1
return value
}
function Effect_CaptionRatio11704(level){
function SCR_REINFORCEABILITY_TOOLTIP(skill) {
    var addAbilRate = 1;

    if ("Matador20" != "None") {
        var reinforceAbil = GetAbility(pc, "Matador20")

        if (reinforceAbil != null) {
            var abilLevel = TryGetProp(reinforceAbil, "Level")
            var masterAddValue = 0

            if (abilLevel == 100) {
                masterAddValue = 0.1
            }

            addAbilRate = 1 + (reinforceAbil.Level * 0.005 + masterAddValue);
            var hidden_abil_cls = GetClass("HiddenAbility_Reinforce", skill.ClassName);

            if (abilLevel >= 65  &&  hidden_abil_cls != null) {
                var hidden_abil_name = TryGetProp(hidden_abil_cls, "HiddenReinforceAbil");
                var hidden_abil = GetAbility(pc, hidden_abil_name);

                if (hidden_abil != null) {
                    var abil_level = TryGetProp(hidden_abil, "Level");
                    var add_factor = TryGetProp(hidden_abil_cls, "FactorByLevel", 0) * 0.01;
                    var add_value = 0;

                    if (abil_level == 10) {
                        add_value = TryGetProp(hidden_abil_cls, "AddFactor", 0) * 0.01
                    }

                    addAbilRate = addAbilRate * (1 + (abil_level * add_factor) + add_value);
                }

            }

        }

    }

    return addAbilRate
}

var value = 10 + (skill.Level * 3)
value = Math.floor(value * SCR_REINFORCEABILITY_TOOLTIP(skill))
return Math.floor(value);
}
function Effect_CaptionRatio11707(){
var value = 15

if (IsPVPField(pc) == 1  &&  value > 2) {
    value = Math.floor((Math.pow(Math.max(0, value-2), 0.5)))+Math.min(2, value)
}

return value
}
function Effect_CaptionRatio11801(level){
var value = skill.Level * 20
return value;
}
function Effect_CaptionRatio11806(level){
var value = 65 + skill.Level * 5
return value;
}
function Effect_CaptionRatio11903(level){
function SCR_REINFORCEABILITY_TOOLTIP(skill) {
    var addAbilRate = 1;

    if ("Retiarii3" != "None") {
        var reinforceAbil = GetAbility(pc, "Retiarii3")

        if (reinforceAbil != null) {
            var abilLevel = TryGetProp(reinforceAbil, "Level")
            var masterAddValue = 0

            if (abilLevel == 100) {
                masterAddValue = 0.1
            }

            addAbilRate = 1 + (reinforceAbil.Level * 0.005 + masterAddValue);
            var hidden_abil_cls = GetClass("HiddenAbility_Reinforce", skill.ClassName);

            if (abilLevel >= 65  &&  hidden_abil_cls != null) {
                var hidden_abil_name = TryGetProp(hidden_abil_cls, "HiddenReinforceAbil");
                var hidden_abil = GetAbility(pc, hidden_abil_name);

                if (hidden_abil != null) {
                    var abil_level = TryGetProp(hidden_abil, "Level");
                    var add_factor = TryGetProp(hidden_abil_cls, "FactorByLevel", 0) * 0.01;
                    var add_value = 0;

                    if (abil_level == 10) {
                        add_value = TryGetProp(hidden_abil_cls, "AddFactor", 0) * 0.01
                    }

                    addAbilRate = addAbilRate * (1 + (abil_level * add_factor) + add_value);
                }

            }

        }

    }

    return addAbilRate
}

var value = skill.Level * 10;
value = Math.floor(value * SCR_REINFORCEABILITY_TOOLTIP(skill))
return value;
}
function Effect_CaptionRatio11907(level){
var value = 10 + skill.Level * 2
return value;
}
function Effect_CaptionRatio12002(level){
var value = 5 * skill.Level
return value;
}
function Effect_CaptionRatio12007(level){
var value = skill.Level * 3
return value
}
function Effect_CaptionRatio12008(){
var value = 2.5

if (IsBuffApplied(pc, "Frenzy_Buff") == "YES") {
    value = 4
}

return value
}
function Effect_CaptionRatio12106(level){
var value = 10 + 9 * skill.Level
return value
}
function Effect_CaptionRatio20002(level){
var value = skill.Level * 2
var abil = GetAbility(pc, "Wizard27")

if (abil != null  &&  abil.ActiveState == 1) {
    value = value * (1 + (abil.Level * 0.005))
}

return Math.floor(value)
}
function Effect_CaptionRatio20003(level){
var value = skill.Level
var zone = GetZoneName(pc);

if (IsPVPServer(pc) == 1  ||  IsPVPField(pc) == 1) {
    value = 1;
}

return value;
}
function Effect_CaptionRatio20004(level){
function SCR_REINFORCEABILITY_TOOLTIP(skill) {
    var addAbilRate = 1;

    if ("Wizard26" != "None") {
        var reinforceAbil = GetAbility(pc, "Wizard26")

        if (reinforceAbil != null) {
            var abilLevel = TryGetProp(reinforceAbil, "Level")
            var masterAddValue = 0

            if (abilLevel == 100) {
                masterAddValue = 0.1
            }

            addAbilRate = 1 + (reinforceAbil.Level * 0.005 + masterAddValue);
            var hidden_abil_cls = GetClass("HiddenAbility_Reinforce", skill.ClassName);

            if (abilLevel >= 65  &&  hidden_abil_cls != null) {
                var hidden_abil_name = TryGetProp(hidden_abil_cls, "HiddenReinforceAbil");
                var hidden_abil = GetAbility(pc, hidden_abil_name);

                if (hidden_abil != null) {
                    var abil_level = TryGetProp(hidden_abil, "Level");
                    var add_factor = TryGetProp(hidden_abil_cls, "FactorByLevel", 0) * 0.01;
                    var add_value = 0;

                    if (abil_level == 10) {
                        add_value = TryGetProp(hidden_abil_cls, "AddFactor", 0) * 0.01
                    }

                    addAbilRate = addAbilRate * (1 + (abil_level * add_factor) + add_value);
                }

            }

        }

    }

    return addAbilRate
}

var value = (skill.Level * 3)
value = value * SCR_REINFORCEABILITY_TOOLTIP(skill)
return value
}
function Effect_CaptionRatio20006(level){
var value = skill.Level - 1
return value
}
function Effect_CaptionRatio20102(){
var value = 5
var abil = GetAbility(pc, "Pyromancer31")

if (abil != null  &&  TryGetProp(abil, "ActiveState", 0) == 1) {
    value = value * 2
}

return value
}
function Effect_CaptionRatio20106(){
var value = 20
var bylvCorrect = pc.Lv - 300

if (bylvCorrect < 0) {
    bylvCorrect = bylvCorrect * 2.75 / 1000
} else if (bylvCorrect >= 0) {
    bylvCorrect = bylvCorrect * 1.25 / 1000
}

value = value * (1 + bylvCorrect)
var abil = GetAbility(pc, 'Pyromancer4')

if (abil != null  &&  abil.ActiveState == 1) {
    value = value * 1.3
}

return Math.floor(value)
}
function Effect_CaptionRatio20109(){
var abil = GetAbility(pc, "Elementalist26")
var value = 4

if (abil != null  &&  abil.ActiveState == 1) {
    value = value + abil.Level
}

return value
}
function Effect_CaptionRatio20201(){
var value = 30
var abilCryomancer2 = GetAbility(pc, 'Cryomancer2');

if (abilCryomancer2 != null  &&  TryGetProp(abilCryomancer2, "ActiveState") == 1  &&  (IsPVPServer(pc) == 0  ||  IsPVPField(pc) == 0)) {
    value = value * (1 + abilCryomancer2.Level * 0.1);
}

var abilCryomancer9 = GetAbility(pc, "Cryomancer9");

if (abilCryomancer9 != null  &&  TryGetProp(abilCryomancer9, "ActiveState") == 1) {
    value = Math.floor(value * (1 + abilCryomancer9.Level * 0.05));
}

return value;
}
function Effect_CaptionRatio20202(){
var value = 10

if (IsPVPField(pc) == 1  &&  value > 2) {
    value = Math.floor((Math.pow(Math.max(0, value-2), 0.5)))+Math.min(2, value)
}

return value
}
function Effect_CaptionRatio20203(level){
return 1 + skill.Level * 1
}
function Effect_CaptionRatio20205(){
var value = 3;
var abil = GetAbility(pc, "Cryomancer7")

if (abil != null  &&  1 == abil.ActiveState) {
    value = value + abil.Level * 0.5
}


if (IsPVPServer(pc) == 1  ||  IsPVPField(pc) == 1) {
    value = value / 2
}

return value
}
function Effect_CaptionRatio20206(level){
var value = 5 + skill.Level;
return value
}
function Effect_CaptionRatio20207(level){
var value = skill.Level * 2

if (IsPVPField(pc) == 1  &&  value > 2) {
    value = Math.floor((Math.pow(Math.max(0, value-2), 0.5)))+Math.min(2, value)
}

return Math.floor(value);
}
function Effect_CaptionRatio20301(level){
var value = skill.Level + 4

if (IsPVPField(pc) == 1  &&  value > 2) {
    value = Math.floor((Math.pow(Math.max(0, value-2), 0.5)))+Math.min(2, value)
}

return value
}
function Effect_CaptionRatio20302(level){
var abil = GetAbility(pc, 'Psychokino1');

if (abil != null  &&  1 == abil.ActiveState) {
    return Math.ceil(0.5 * skill.Level) + abil.Level;
}

return Math.ceil(0.5 * skill.Level)
}
function Effect_CaptionRatio20303(level){
var value = skill.Level
return value;
}
function Effect_CaptionRatio20304(level){
var value = 100 + skill.Level * 20;

if (IsBuffApplied(pc, "Thurisaz_Buff") == "YES") {
    value = value * 1.5
}

return value
}
function Effect_CaptionRatio20306(level){
var value = skill.Level;

if (IsPVPField(pc) == 1  &&  value > 2) {
    value = Math.floor((Math.pow(Math.max(0, value-2), 0.5)))+Math.min(2, value)
}

return value;
}
function Effect_CaptionRatio20307(level){
var value = 10 + skill.Level * 1

if (IsPVPField(pc) == 1  &&  value > 2) {
    value = Math.floor((Math.pow(Math.max(0, value-2), 0.5)))+Math.min(2, value)
}

return value
}
function Effect_CaptionRatio20601(level){
var value = 1 + (2 + skill.Level * 0.5)

if (IsPVPField(pc) == 1  &&  value > 2) {
    value = Math.floor((Math.pow(Math.max(0, value-2), 0.5)))+Math.min(2, value)
}

return Math.floor(value);
}
function Effect_CaptionRatio20606(){
var value = 0;
var abil = GetAbility(pc, 'Elementalist9')

if (abil != null  &&  1 == abil.ActiveState) {
    value = value + abil.Level * 5;
}

return value;
}
function Effect_CaptionRatio20701(level){
var value = 16 + (skill.Level * 5.6);
return value;
}
function Effect_CaptionRatio20703(){
var value = 50
return value
}
function Effect_CaptionRatio20707(level){
var value = 14.72 + (skill.Level * 5.152);
return value;
}
function Effect_CaptionRatio20708(level){
var value = skill.Level

if (value > 5) {
    value = 5
}

return value
}
function Effect_CaptionRatio20710(level){
var value = 210 + (skill.Level-1) * 10
return value
}
function Effect_CaptionRatio20804(level){
return Math.floor(8 + skill.Level * 1.5);
}
function Effect_CaptionRatio20806(level){
return 50 + skill.Level * 10
}
function Effect_CaptionRatio20808(level){
var value = 5 * skill.Level

if (value > 90) {
    value = 90
}

return value
}
function Effect_CaptionRatio20809(level){
var value = skill.Level * 3
return value;
}
function Effect_CaptionRatio20901(level){
var value = 210 + (skill.Level-1) * 10
return value
}
function Effect_CaptionRatio20902(level){
var value = skill.Level * 23;
return Math.floor(value);
}
function Effect_CaptionRatio20903(){
var value = 15
return value
}
function Effect_CaptionRatio20904(){
var value = 5
return value
}
function Effect_CaptionRatio20905(level){
var value = 2 + skill.Level
return value
}
function Effect_CaptionRatio20906(){
var value = 70;
return value
}
function Effect_CaptionRatio20907(level){
var value = 20 + skill.Level * 2

if (IsPVPServer(pc) == 1) {
    value = 900
}

return value
}
function Effect_CaptionRatio20909(level){
var value = skill.Level * 18.4;
return Math.floor(value);
}
function Effect_CaptionRatio20910(level){
var value = skill.Level * 10
return value;
}
function Effect_CaptionRatio20911(level){
var value = skill.Level * 23;
return Math.floor(value);
}
function Effect_CaptionRatio20912(level){
var value = skill.Level * 23;
return Math.floor(value);
}
function Effect_CaptionRatio21002(level){
var value = skill.Level;
return value;
}
function Effect_CaptionRatio21003(level){
var value = skill.Level * 1

if (value > 10) {
    value = 10
}

return value
}
function Effect_CaptionRatio21004(level){
var value = 4.5 + skill.Level * 0.5;
return value
}
function Effect_CaptionRatio21006(level){
var value = 2 + skill.Level;

if (value > 7) {
    value = 7;
}

return Math.floor(value)
}
function Effect_CaptionRatio21009(level){
var numberArg1 = 395 // @rjgtav. using Lv 15 Condensed HP Potion
var hpValue = numberArg1 * 7
hpValue = hpValue * 8
var sprinkleHP = hpValue * (skill.Level * 0.1)
return sprinkleHP;
}
function Effect_CaptionRatio21010(level){
var numberArg1 = 131 // @rjgtav. using Lv 15 Condensed SP Potion
var spValue = numberArg1 * 7
spValue = spValue * 8
var sprinkleSP = spValue * (skill.Level * 0.1)
return sprinkleSP;
}
function Effect_CaptionRatio21103(level){
var value = 30 + skill.Level * 10
return Math.floor(value)
}
function Effect_CaptionRatio21107(){
var value = 30;
return value;
}
function Effect_CaptionRatio21108(){
var value = 30
var abil = GetAbility(pc, 'Featherfoot12')

if (abil != null  &&  1 == abil.ActiveState) {
    value = 20
}

return value;
}
function Effect_CaptionRatio21206(level){
var value = skill.Level
return value
}
function Effect_CaptionRatio21207(){
var value = 50
value = value + (TryGetProp(skill, "Level") * 10)
return value
}
function Effect_CaptionRatio21305(level){
function SCR_REINFORCEABILITY_TOOLTIP(skill) {
    var addAbilRate = 1;

    if ("RuneCaster10" != "None") {
        var reinforceAbil = GetAbility(pc, "RuneCaster10")

        if (reinforceAbil != null) {
            var abilLevel = TryGetProp(reinforceAbil, "Level")
            var masterAddValue = 0

            if (abilLevel == 100) {
                masterAddValue = 0.1
            }

            addAbilRate = 1 + (reinforceAbil.Level * 0.005 + masterAddValue);
            var hidden_abil_cls = GetClass("HiddenAbility_Reinforce", skill.ClassName);

            if (abilLevel >= 65  &&  hidden_abil_cls != null) {
                var hidden_abil_name = TryGetProp(hidden_abil_cls, "HiddenReinforceAbil");
                var hidden_abil = GetAbility(pc, hidden_abil_name);

                if (hidden_abil != null) {
                    var abil_level = TryGetProp(hidden_abil, "Level");
                    var add_factor = TryGetProp(hidden_abil_cls, "FactorByLevel", 0) * 0.01;
                    var add_value = 0;

                    if (abil_level == 10) {
                        add_value = TryGetProp(hidden_abil_cls, "AddFactor", 0) * 0.01
                    }

                    addAbilRate = addAbilRate * (1 + (abil_level * add_factor) + add_value);
                }

            }

        }

    }

    return addAbilRate
}

var value = 5 + skill.Level * 1
value = value * SCR_REINFORCEABILITY_TOOLTIP(skill);
return value;
}
function Effect_CaptionRatio21308(level){
function SCR_REINFORCEABILITY_TOOLTIP(skill) {
    var addAbilRate = 1;

    if ("RuneCaster25" != "None") {
        var reinforceAbil = GetAbility(pc, "RuneCaster25")

        if (reinforceAbil != null) {
            var abilLevel = TryGetProp(reinforceAbil, "Level")
            var masterAddValue = 0

            if (abilLevel == 100) {
                masterAddValue = 0.1
            }

            addAbilRate = 1 + (reinforceAbil.Level * 0.005 + masterAddValue);
            var hidden_abil_cls = GetClass("HiddenAbility_Reinforce", skill.ClassName);

            if (abilLevel >= 65  &&  hidden_abil_cls != null) {
                var hidden_abil_name = TryGetProp(hidden_abil_cls, "HiddenReinforceAbil");
                var hidden_abil = GetAbility(pc, hidden_abil_name);

                if (hidden_abil != null) {
                    var abil_level = TryGetProp(hidden_abil, "Level");
                    var add_factor = TryGetProp(hidden_abil_cls, "FactorByLevel", 0) * 0.01;
                    var add_value = 0;

                    if (abil_level == 10) {
                        add_value = TryGetProp(hidden_abil_cls, "AddFactor", 0) * 0.01
                    }

                    addAbilRate = addAbilRate * (1 + (abil_level * add_factor) + add_value);
                }

            }

        }

    }

    return addAbilRate
}

var value = 15 + skill.Level * 1
value = value * SCR_REINFORCEABILITY_TOOLTIP(skill);
return value;
}
function Effect_CaptionRatio21401(){
var value = 3
var abil1 = GetAbility(pc, "Sage1")

if (abil1 != null  &&  1 == abil1.ActiveState) {
    value = value + abil1.Level
}

var abil2 = GetAbility(pc, "Sage16")

if (abil2 != null  &&  1 == abil2.ActiveState) {
    value = value + abil2.Level
}

var abil3 = GetAbility(pc, "Sage17")

if (abil3 != null  &&  1 == abil3.ActiveState) {
    value = value + abil3.Level
}

return value;
}
function Effect_CaptionRatio21405(level){
var value = 100 + skill.Level * 10
return value
}
function Effect_CaptionRatio21411(){
var value = 10

if (IsPVPField(pc) == 1  &&  value > 2) {
    value = Math.floor((Math.pow(Math.max(0, value-2), 0.5)))+Math.min(2, value)
}

return Math.floor(value)
}
function Effect_CaptionRatio21602(){
var value = 10

if (IsPVPField(pc) == 1  &&  value > 2) {
    value = Math.floor((Math.pow(Math.max(0, value-2), 0.5)))+Math.min(2, value)
}

return value
}
function Effect_CaptionRatio21604(level){
var value = 25 + (skill.Level * 5)

if ("Shadowmancer10" != "None") {
    var reinforceAbil = GetAbility(pc, "Shadowmancer10")

    if (reinforceAbil != null) {
        var abilLevel = TryGetProp(reinforceAbil, "Level")
        value = value * (1 + (reinforceAbil.Level * 0.005));
    }

}

return value
}
function Effect_CaptionRatio21605(){
var value = 5

if (IsPVPField(pc) == 1  &&  value > 2) {
    value = Math.floor((Math.pow(Math.max(0, value-2), 0.5)))+Math.min(2, value)
}

return value
}
function Effect_CaptionRatio21606(level){
var value = 20 + skill.Level * 2
return value
}
function Effect_CaptionRatio21613(level){
var value = 20 + (skill.Level -1) * 20;

if (value > 120) {
    value = 120
}

return value
}
function Effect_CaptionRatio21608(){
var value = 10

if (IsPVPField(pc) == 1  &&  value > 2) {
    value = Math.floor((Math.pow(Math.max(0, value-2), 0.5)))+Math.min(2, value)
}

return value
}
function Effect_CaptionRatio21609(level){
var value = 4 + skill.Level

if (IsPVPField(pc) == 1  &&  value > 2) {
    value = Math.floor((Math.pow(Math.max(0, value-2), 0.5)))+Math.min(2, value)
}

return value
}
function Effect_CaptionRatio21610(){
var value = 12
return value
}
function Effect_CaptionRatio21611(level){
var SPValue = 10

if (IsPVPField(pc) == 1) {
    SPValue = 5
}

var value = 100 - ((skill.Level - 1) * SPValue)
var abilOnmyoji12 = GetAbility(pc, "Onmyoji12")

if (abilOnmyoji12 != null  &&  TryGetProp(abilOnmyoji12, "ActiveState", 0) == 1) {
    value = value - (value * abilOnmyoji12.Level * 0.01)
}

return value
}
function Effect_CaptionRatio21612(){
var value = 15

if (IsPVPField(pc) == 1  &&  value > 2) {
    value = Math.floor((Math.pow(Math.max(0, value-2), 0.5)))+Math.min(2, value)
}

return value
}
function Effect_CaptionRatio21614(){
var value = 15

if (IsPVPField(pc) == 1  &&  value > 2) {
    value = Math.floor((Math.pow(Math.max(0, value-2), 0.5)))+Math.min(2, value)
}

return value
}
function Effect_CaptionRatio21615(){
var value = 7

if (IsPVPField(pc) == 1  &&  value > 2) {
    value = Math.floor((Math.pow(Math.max(0, value-2), 0.5)))+Math.min(2, value)
}

return value
}
function Effect_CaptionRatio21701(level){
var value = 7.5 + (skill.Level * 0.5)
return value;
}
function Effect_CaptionRatio21704(level){
var value = 10 + (skill.Level * 2)
return value;
}
function Effect_CaptionRatio21706(level){
var value = skill.Level
return value
}
function Effect_CaptionRatio21709(level){
var value = skill.Level
return value
}
function Effect_CaptionRatio21801(level){
var value = 40 * (1 + skill.Level * 0.1)
return Math.floor(value)
}
function Effect_CaptionRatio21804(level){
function SCR_REINFORCEABILITY_TOOLTIP(skill) {
    var addAbilRate = 1;

    if ("Daoshi19" != "None") {
        var reinforceAbil = GetAbility(pc, "Daoshi19")

        if (reinforceAbil != null) {
            var abilLevel = TryGetProp(reinforceAbil, "Level")
            var masterAddValue = 0

            if (abilLevel == 100) {
                masterAddValue = 0.1
            }

            addAbilRate = 1 + (reinforceAbil.Level * 0.005 + masterAddValue);
            var hidden_abil_cls = GetClass("HiddenAbility_Reinforce", skill.ClassName);

            if (abilLevel >= 65  &&  hidden_abil_cls != null) {
                var hidden_abil_name = TryGetProp(hidden_abil_cls, "HiddenReinforceAbil");
                var hidden_abil = GetAbility(pc, hidden_abil_name);

                if (hidden_abil != null) {
                    var abil_level = TryGetProp(hidden_abil, "Level");
                    var add_factor = TryGetProp(hidden_abil_cls, "FactorByLevel", 0) * 0.01;
                    var add_value = 0;

                    if (abil_level == 10) {
                        add_value = TryGetProp(hidden_abil_cls, "AddFactor", 0) * 0.01
                    }

                    addAbilRate = addAbilRate * (1 + (abil_level * add_factor) + add_value);
                }

            }

        }

    }

    return addAbilRate
}

var value = skill.Level * 5
value = value * SCR_REINFORCEABILITY_TOOLTIP(skill);
return Math.floor(value);
}
function Effect_CaptionRatio21805(){
var value = 10
var abilDaoshi37 = GetAbility(owner, "Daoshi37")

if (abilDaoshi37 != null  &&  TryGetProp(abilDaoshi37, "ActiveState", 0) == 1) {
    value = 5
}

return value;
}
function Effect_CaptionRatio21809(){
function SCR_REINFORCEABILITY_TOOLTIP(skill) {
    var addAbilRate = 1;

    if ("Daoshi15" != "None") {
        var reinforceAbil = GetAbility(pc, "Daoshi15")

        if (reinforceAbil != null) {
            var abilLevel = TryGetProp(reinforceAbil, "Level")
            var masterAddValue = 0

            if (abilLevel == 100) {
                masterAddValue = 0.1
            }

            addAbilRate = 1 + (reinforceAbil.Level * 0.005 + masterAddValue);
            var hidden_abil_cls = GetClass("HiddenAbility_Reinforce", skill.ClassName);

            if (abilLevel >= 65  &&  hidden_abil_cls != null) {
                var hidden_abil_name = TryGetProp(hidden_abil_cls, "HiddenReinforceAbil");
                var hidden_abil = GetAbility(pc, hidden_abil_name);

                if (hidden_abil != null) {
                    var abil_level = TryGetProp(hidden_abil, "Level");
                    var add_factor = TryGetProp(hidden_abil_cls, "FactorByLevel", 0) * 0.01;
                    var add_value = 0;

                    if (abil_level == 10) {
                        add_value = TryGetProp(hidden_abil_cls, "AddFactor", 0) * 0.01
                    }

                    addAbilRate = addAbilRate * (1 + (abil_level * add_factor) + add_value);
                }

            }

        }

    }

    return addAbilRate
}

var value = 45 + TryGetProp(skill, "Level", 1) * 1
value = value * SCR_REINFORCEABILITY_TOOLTIP(skill);
return value
}
function Effect_CaptionRatio21902(level){
var value = 10 + skill.Level
return value
}
function Effect_CaptionRatio21906(){
var value = 10

if (IsPVPField(pc) == 1  &&  value > 2) {
    value = Math.floor((Math.pow(Math.max(0, value-2), 0.5)))+Math.min(2, value)
}

return value
}
function Effect_CaptionRatio30001(){
var value = 10;
return value
}
function Effect_CaptionRatio30005(){
var value = 50
return Math.floor(value)
}
function Effect_CaptionRatio30008(level){
function SCR_REINFORCEABILITY_TOOLTIP(skill) {
    var addAbilRate = 1;

    if ("Archer34" != "None") {
        var reinforceAbil = GetAbility(pc, "Archer34")

        if (reinforceAbil != null) {
            var abilLevel = TryGetProp(reinforceAbil, "Level")
            var masterAddValue = 0

            if (abilLevel == 100) {
                masterAddValue = 0.1
            }

            addAbilRate = 1 + (reinforceAbil.Level * 0.005 + masterAddValue);
            var hidden_abil_cls = GetClass("HiddenAbility_Reinforce", skill.ClassName);

            if (abilLevel >= 65  &&  hidden_abil_cls != null) {
                var hidden_abil_name = TryGetProp(hidden_abil_cls, "HiddenReinforceAbil");
                var hidden_abil = GetAbility(pc, hidden_abil_name);

                if (hidden_abil != null) {
                    var abil_level = TryGetProp(hidden_abil, "Level");
                    var add_factor = TryGetProp(hidden_abil_cls, "FactorByLevel", 0) * 0.01;
                    var add_value = 0;

                    if (abil_level == 10) {
                        add_value = TryGetProp(hidden_abil_cls, "AddFactor", 0) * 0.01
                    }

                    addAbilRate = addAbilRate * (1 + (abil_level * add_factor) + add_value);
                }

            }

        }

    }

    return addAbilRate
}

var value = 2 * skill.Level;
value = value * SCR_REINFORCEABILITY_TOOLTIP(skill);
return value;
}
function Effect_CaptionRatio30009(level){
var value = 120 + (skill.Level * 10)
return value;
}
function Effect_CaptionRatio30103(level){
var value = 25 + skill.Level * 2.5
return value
}
function Effect_CaptionRatio30106(){
var value = 6;
return value
}
function Effect_CaptionRatio30107(){
return 6;
}
function Effect_CaptionRatio30201(level){
var value = 15 + skill.Level * 5;

if (IsPVPField(pc) == 1) {
    value = 15;
} else {
    var abil = GetAbility(pc, 'QuarrelShooter24')

    if (abil != null  &&  abil.ActiveState == 1) {
        value = Math.ceil(value * 0.5)
    }

}

return value;
}
function Effect_CaptionRatio30203(level){
var value = skill.Level
return value
}
function Effect_CaptionRatio30204(level){
var value = 25 + skill.Level * 5

if (value >= 100) {
    value = 100
}

return value
}
function Effect_CaptionRatio30208(){
function SCR_REINFORCEABILITY_TOOLTIP(skill) {
    var addAbilRate = 1;

    if ("Archer14" != "None") {
        var reinforceAbil = GetAbility(pc, "Archer14")

        if (reinforceAbil != null) {
            var abilLevel = TryGetProp(reinforceAbil, "Level")
            var masterAddValue = 0

            if (abilLevel == 100) {
                masterAddValue = 0.1
            }

            addAbilRate = 1 + (reinforceAbil.Level * 0.005 + masterAddValue);
            var hidden_abil_cls = GetClass("HiddenAbility_Reinforce", skill.ClassName);

            if (abilLevel >= 65  &&  hidden_abil_cls != null) {
                var hidden_abil_name = TryGetProp(hidden_abil_cls, "HiddenReinforceAbil");
                var hidden_abil = GetAbility(pc, hidden_abil_name);

                if (hidden_abil != null) {
                    var abil_level = TryGetProp(hidden_abil, "Level");
                    var add_factor = TryGetProp(hidden_abil_cls, "FactorByLevel", 0) * 0.01;
                    var add_value = 0;

                    if (abil_level == 10) {
                        add_value = TryGetProp(hidden_abil_cls, "AddFactor", 0) * 0.01
                    }

                    addAbilRate = addAbilRate * (1 + (abil_level * add_factor) + add_value);
                }

            }

        }

    }

    return addAbilRate
}

var value = 15;
value = value * SCR_REINFORCEABILITY_TOOLTIP(skill);
return value;
}
function Effect_CaptionRatio30209(level){
var value = skill.Level * 10
return value
}
function Effect_CaptionRatio30302(){
var value = 5
return value
}
function Effect_CaptionRatio30304(){
var value = 4
var abil = GetAbility(pc, "Sapper4")

if (abil != null  &&  1 == abil.ActiveState) {
    value = value + abil.Level;
}

return Math.floor(value)
}
function Effect_CaptionRatio30307(level){
return skill.Level
}
function Effect_CaptionRatio30401(level){
var value = 5 + skill.Level * 0.5;
return value
}
function Effect_CaptionRatio30405(level){
return 10 + skill.Level * 6
}
function Effect_CaptionRatio30407(level){
var value = skill.Level * 200
return value;
}
function Effect_CaptionRatio30408(level){
var value = skill.Level * 1.5
return value
}
function Effect_CaptionRatio30409(level){
function SCR_REINFORCEABILITY_TOOLTIP(skill) {
    var addAbilRate = 1;

    if ("Hunter14" != "None") {
        var reinforceAbil = GetAbility(pc, "Hunter14")

        if (reinforceAbil != null) {
            var abilLevel = TryGetProp(reinforceAbil, "Level")
            var masterAddValue = 0

            if (abilLevel == 100) {
                masterAddValue = 0.1
            }

            addAbilRate = 1 + (reinforceAbil.Level * 0.005 + masterAddValue);
            var hidden_abil_cls = GetClass("HiddenAbility_Reinforce", skill.ClassName);

            if (abilLevel >= 65  &&  hidden_abil_cls != null) {
                var hidden_abil_name = TryGetProp(hidden_abil_cls, "HiddenReinforceAbil");
                var hidden_abil = GetAbility(pc, hidden_abil_name);

                if (hidden_abil != null) {
                    var abil_level = TryGetProp(hidden_abil, "Level");
                    var add_factor = TryGetProp(hidden_abil_cls, "FactorByLevel", 0) * 0.01;
                    var add_value = 0;

                    if (abil_level == 10) {
                        add_value = TryGetProp(hidden_abil_cls, "AddFactor", 0) * 0.01
                    }

                    addAbilRate = addAbilRate * (1 + (abil_level * add_factor) + add_value);
                }

            }

        }

    }

    return addAbilRate
}

var value = skill.Level * 4
value = value * SCR_REINFORCEABILITY_TOOLTIP(skill);
return Math.floor(value);
}
function Effect_CaptionRatio30503(level){
return 2 + skill.Level
}
function Effect_CaptionRatio30510(level){
var value = 4 * skill.Level
return value;
}
function Effect_CaptionRatio30601(level){
var value = skill.Level * 5
return Math.floor(value);
}
function Effect_CaptionRatio30602(){
var value = 5;
var Scout6_abil =  GetAbility(pc, 'Scout6')

if (Scout6_abil != null  &&  1 == Scout6_abil.ActiveState) {
    value = value + (Scout6_abil.Level * 1)
}

return value;
}
function Effect_CaptionRatio30605(level){
var value = 55 + skill.Level *5;
return value
}
function Effect_CaptionRatio30607(level){
var value = 5 * skill.Level * 1;
return Math.floor(value);
}
function Effect_CaptionRatio30802(level){
var value = 7.5 + (skill.Level * 1.5)
return value;
}
function Effect_CaptionRatio31003(level){
var value = skill.Level
var abil = GetAbility(pc, "Falconer11");

if (abil != null  &&  1 == abil.ActiveState) {
    value = value + 3
}

return value
}
function Effect_CaptionRatio31004(){
var value = 10;
var abil = GetAbility(pc, "Falconer3")

if (abil != null  &&  1 == abil.ActiveState) {
    value = value + abil.Level * 3
}

return value
}
function Effect_CaptionRatio31006(level){
return 30 + (skill.Level-1) * 5
}
function Effect_CaptionRatio31012(){
var lv = pc.Lv
var bylvCorrect = lv - 300
var spendSP = 90

if (bylvCorrect < 0) {
    bylvCorrect = bylvCorrect * 2.75 / 1000
} else if (bylvCorrect >= 0) {
    bylvCorrect = bylvCorrect * 1.25 / 1000
}

var skillLv = TryGetProp(skill, "Level", 1)
var spendSP = spendSP * (1 + bylvCorrect) * (1 - ((skillLv - 1) * 0.1))
return Math.floor(spendSP)
}
function Effect_CaptionRatio31209(level){
var value = 4 - (skill.Level * 0.72)

if (value < 0.4) {
    value = 0.4
}

return value;
}
function Effect_CaptionRatio31408(level){
var value = 3.5 + skill.Level * 0.5;
return value;
}
function Effect_CaptionRatio31502(level){
return skill.Level + 2
}
function Effect_CaptionRatio31505(level){
return 10 + (skill.Level * 2);
}
function Effect_CaptionRatio31506(level){
function SCR_REINFORCEABILITY_TOOLTIP(skill) {
    var addAbilRate = 1;

    if ("Appraiser5" != "None") {
        var reinforceAbil = GetAbility(pc, "Appraiser5")

        if (reinforceAbil != null) {
            var abilLevel = TryGetProp(reinforceAbil, "Level")
            var masterAddValue = 0

            if (abilLevel == 100) {
                masterAddValue = 0.1
            }

            addAbilRate = 1 + (reinforceAbil.Level * 0.005 + masterAddValue);
            var hidden_abil_cls = GetClass("HiddenAbility_Reinforce", skill.ClassName);

            if (abilLevel >= 65  &&  hidden_abil_cls != null) {
                var hidden_abil_name = TryGetProp(hidden_abil_cls, "HiddenReinforceAbil");
                var hidden_abil = GetAbility(pc, hidden_abil_name);

                if (hidden_abil != null) {
                    var abil_level = TryGetProp(hidden_abil, "Level");
                    var add_factor = TryGetProp(hidden_abil_cls, "FactorByLevel", 0) * 0.01;
                    var add_value = 0;

                    if (abil_level == 10) {
                        add_value = TryGetProp(hidden_abil_cls, "AddFactor", 0) * 0.01
                    }

                    addAbilRate = addAbilRate * (1 + (abil_level * add_factor) + add_value);
                }

            }

        }

    }

    return addAbilRate
}

var value = skill.Level * 6
value = Math.floor(value * SCR_REINFORCEABILITY_TOOLTIP(skill))
return value;
}
function Effect_CaptionRatio31508(level){
function SCR_REINFORCEABILITY_TOOLTIP(skill) {
    var addAbilRate = 1;

    if ("Appraiser12" != "None") {
        var reinforceAbil = GetAbility(pc, "Appraiser12")

        if (reinforceAbil != null) {
            var abilLevel = TryGetProp(reinforceAbil, "Level")
            var masterAddValue = 0

            if (abilLevel == 100) {
                masterAddValue = 0.1
            }

            addAbilRate = 1 + (reinforceAbil.Level * 0.005 + masterAddValue);
            var hidden_abil_cls = GetClass("HiddenAbility_Reinforce", skill.ClassName);

            if (abilLevel >= 65  &&  hidden_abil_cls != null) {
                var hidden_abil_name = TryGetProp(hidden_abil_cls, "HiddenReinforceAbil");
                var hidden_abil = GetAbility(pc, hidden_abil_name);

                if (hidden_abil != null) {
                    var abil_level = TryGetProp(hidden_abil, "Level");
                    var add_factor = TryGetProp(hidden_abil_cls, "FactorByLevel", 0) * 0.01;
                    var add_value = 0;

                    if (abil_level == 10) {
                        add_value = TryGetProp(hidden_abil_cls, "AddFactor", 0) * 0.01
                    }

                    addAbilRate = addAbilRate * (1 + (abil_level * add_factor) + add_value);
                }

            }

        }

    }

    return addAbilRate
}

var value = skill.Level * 4
value = value * SCR_REINFORCEABILITY_TOOLTIP(skill)
return value;
}
function Effect_CaptionRatio31701(){
var value = 5

if (IsPVPServer(pc) == 1  ||  IsPVPField(pc) == 1) {
    value = value / 2
}

return value;
}
function Effect_CaptionRatio31702(level){
var value = 5 + skill.Level
return value;
}
function Effect_CaptionRatio31703(level){
var value = 3 + skill.Level
return value;
}
function Effect_CaptionRatio31705(level){
var value = 4 + skill.Level

if (IsPVPField(pc) == 1  &&  value > 2) {
    value = Math.floor((Math.pow(Math.max(0, value-2), 0.5)))+Math.min(2, value)
}

return value;
}
function Effect_CaptionRatio31706(level){
var value = 10 + skill.Level
return value;
}
function Effect_CaptionRatio31707(level){
var value = 50 + (skill.Level * 10)
return value;
}
function Effect_CaptionRatio31801(){
var value = 90;
var abil = GetAbility(pc, "Matross2")

if (abil != null  &&  abil.ActiveState == 1) {
    value = 45
}

return value
}
function Effect_CaptionRatio31802(level){
var value = Math.floor(3 + skill.Level * 0.375);

if (IsBuffApplied(pc, "Bazooka_Buff") == "YES") {
    value = value * 2
}


if (IsPVPField(pc) == 1  &&  value > 2) {
    value = Math.floor((Math.pow(Math.max(0, value-2), 0.5)))+Math.min(2, value)
}

return value
}
function Effect_CaptionRatio31803(level){
var value = 3 + skill.Level;

if (IsPVPField(pc) == 1  &&  value > 2) {
    value = Math.floor((Math.pow(Math.max(0, value-2), 0.5)))+Math.min(2, value)
}

return value;
}
function Effect_CaptionRatio31805(level){
var value = 30 + skill.Level * 3
return value
}
function Effect_CaptionRatio31806(){
var value = 10

if (IsPVPField(pc) == 1  &&  value > 2) {
    value = Math.floor((Math.pow(Math.max(0, value-2), 0.5)))+Math.min(2, value)
}

return value
}
function Effect_CaptionRatio31902(level){
var value = 20 * skill.Level

if (value >= 100) {
    value = 100
}

return value
}
function Effect_CaptionRatio31904(level){
var value = 10 + skill.Level * 2
return value
}
function Effect_CaptionRatio31905(level){
var value = skill.Level * 5
return value
}
function Effect_CaptionRatio31906(level){
var value = 50 - (skill.Level * 3)
return value
}
function Effect_CaptionRatio32004(level){
var value = skill.Level * 5
return value
}
function Effect_CaptionRatio32005(){
var value = 3
var abil = GetAbility(pc, 'Arbalester18')

if (abil != null  &&  TryGetProp(abil, 'ActiveState', 0) == 1) {
    value = 7
}


if (IsPVPField(pc) == 1  &&  value > 2) {
    value = Math.floor((Math.pow(Math.max(0, value-2), 0.5)))+Math.min(2, value)
}

return value
}
function Effect_CaptionRatio32006(){
var value = Math.floor(7 + TryGetProp(pc, "SR", 0)/3)

if (IsPVPField(pc) == 1  &&  value > 2) {
    value = Math.floor((Math.pow(Math.max(0, value-2), 0.5)))+Math.min(2, value)
}

return value
}
function Effect_CaptionRatio32101(level){
function SCR_REINFORCEABILITY_TOOLTIP(skill) {
    var addAbilRate = 1;

    if ("Arquebusier1" != "None") {
        var reinforceAbil = GetAbility(pc, "Arquebusier1")

        if (reinforceAbil != null) {
            var abilLevel = TryGetProp(reinforceAbil, "Level")
            var masterAddValue = 0

            if (abilLevel == 100) {
                masterAddValue = 0.1
            }

            addAbilRate = 1 + (reinforceAbil.Level * 0.005 + masterAddValue);
            var hidden_abil_cls = GetClass("HiddenAbility_Reinforce", skill.ClassName);

            if (abilLevel >= 65  &&  hidden_abil_cls != null) {
                var hidden_abil_name = TryGetProp(hidden_abil_cls, "HiddenReinforceAbil");
                var hidden_abil = GetAbility(pc, hidden_abil_name);

                if (hidden_abil != null) {
                    var abil_level = TryGetProp(hidden_abil, "Level");
                    var add_factor = TryGetProp(hidden_abil_cls, "FactorByLevel", 0) * 0.01;
                    var add_value = 0;

                    if (abil_level == 10) {
                        add_value = TryGetProp(hidden_abil_cls, "AddFactor", 0) * 0.01
                    }

                    addAbilRate = addAbilRate * (1 + (abil_level * add_factor) + add_value);
                }

            }

        }

    }

    return addAbilRate
}

var value = 6 * skill.Level
value = value * SCR_REINFORCEABILITY_TOOLTIP(skill)
return value
}
function Effect_CaptionRatio32107(){
var value = 1

if (GetExProp(pc, "ITEM_VIBORA_Arquebusier") > 0) {
    value = value / 2
}

return value
}
function Effect_CaptionRatio39022(level){
var value = skill.Level

if (value > 5) {
    value = 5
}

return value;
}
function Effect_CaptionRatio40002(level){
function SCR_REINFORCEABILITY_TOOLTIP(skill) {
    var addAbilRate = 1;

    if ("Cleric11" != "None") {
        var reinforceAbil = GetAbility(pc, "Cleric11")

        if (reinforceAbil != null) {
            var abilLevel = TryGetProp(reinforceAbil, "Level")
            var masterAddValue = 0

            if (abilLevel == 100) {
                masterAddValue = 0.1
            }

            addAbilRate = 1 + (reinforceAbil.Level * 0.005 + masterAddValue);
            var hidden_abil_cls = GetClass("HiddenAbility_Reinforce", skill.ClassName);

            if (abilLevel >= 65  &&  hidden_abil_cls != null) {
                var hidden_abil_name = TryGetProp(hidden_abil_cls, "HiddenReinforceAbil");
                var hidden_abil = GetAbility(pc, hidden_abil_name);

                if (hidden_abil != null) {
                    var abil_level = TryGetProp(hidden_abil, "Level");
                    var add_factor = TryGetProp(hidden_abil_cls, "FactorByLevel", 0) * 0.01;
                    var add_value = 0;

                    if (abil_level == 10) {
                        add_value = TryGetProp(hidden_abil_cls, "AddFactor", 0) * 0.01
                    }

                    addAbilRate = addAbilRate * (1 + (abil_level * add_factor) + add_value);
                }

            }

        }

    }

    return addAbilRate
}

var value = skill.Level * 10
value = value * SCR_REINFORCEABILITY_TOOLTIP(skill)
return value
}
function Effect_CaptionRatio40003(level){
var value = skill.Level * 2;
var abil = GetAbility(pc, 'Cleric18')

if (abil != null  &&  1 == abil.ActiveState) {
    value = value + abil.Level * 1;
}

return value;
}
function Effect_CaptionRatio40007(level){
function SCR_REINFORCEABILITY_TOOLTIP(skill) {
    var addAbilRate = 1;

    if ("Cleric23" != "None") {
        var reinforceAbil = GetAbility(pc, "Cleric23")

        if (reinforceAbil != null) {
            var abilLevel = TryGetProp(reinforceAbil, "Level")
            var masterAddValue = 0

            if (abilLevel == 100) {
                masterAddValue = 0.1
            }

            addAbilRate = 1 + (reinforceAbil.Level * 0.005 + masterAddValue);
            var hidden_abil_cls = GetClass("HiddenAbility_Reinforce", skill.ClassName);

            if (abilLevel >= 65  &&  hidden_abil_cls != null) {
                var hidden_abil_name = TryGetProp(hidden_abil_cls, "HiddenReinforceAbil");
                var hidden_abil = GetAbility(pc, hidden_abil_name);

                if (hidden_abil != null) {
                    var abil_level = TryGetProp(hidden_abil, "Level");
                    var add_factor = TryGetProp(hidden_abil_cls, "FactorByLevel", 0) * 0.01;
                    var add_value = 0;

                    if (abil_level == 10) {
                        add_value = TryGetProp(hidden_abil_cls, "AddFactor", 0) * 0.01
                    }

                    addAbilRate = addAbilRate * (1 + (abil_level * add_factor) + add_value);
                }

            }

        }

    }

    return addAbilRate
}

var value = skill.Level * 5
value = value * SCR_REINFORCEABILITY_TOOLTIP(skill)
return value;
}
function Effect_CaptionRatio40102(){
function SCR_REINFORCEABILITY_TOOLTIP(skill) {
    var addAbilRate = 1;

    if ("Kriwi17" != "None") {
        var reinforceAbil = GetAbility(pc, "Kriwi17")

        if (reinforceAbil != null) {
            var abilLevel = TryGetProp(reinforceAbil, "Level")
            var masterAddValue = 0

            if (abilLevel == 100) {
                masterAddValue = 0.1
            }

            addAbilRate = 1 + (reinforceAbil.Level * 0.005 + masterAddValue);
            var hidden_abil_cls = GetClass("HiddenAbility_Reinforce", skill.ClassName);

            if (abilLevel >= 65  &&  hidden_abil_cls != null) {
                var hidden_abil_name = TryGetProp(hidden_abil_cls, "HiddenReinforceAbil");
                var hidden_abil = GetAbility(pc, hidden_abil_name);

                if (hidden_abil != null) {
                    var abil_level = TryGetProp(hidden_abil, "Level");
                    var add_factor = TryGetProp(hidden_abil_cls, "FactorByLevel", 0) * 0.01;
                    var add_value = 0;

                    if (abil_level == 10) {
                        add_value = TryGetProp(hidden_abil_cls, "AddFactor", 0) * 0.01
                    }

                    addAbilRate = addAbilRate * (1 + (abil_level * add_factor) + add_value);
                }

            }

        }

    }

    return addAbilRate
}

var value = 15 + TryGetProp(skill, 'Level', 1) * 3
value = value * SCR_REINFORCEABILITY_TOOLTIP(skill);
return value
}
function Effect_CaptionRatio40103(){
function SCR_REINFORCEABILITY_TOOLTIP(skill) {
    var addAbilRate = 1;

    if ("Kriwi32" != "None") {
        var reinforceAbil = GetAbility(pc, "Kriwi32")

        if (reinforceAbil != null) {
            var abilLevel = TryGetProp(reinforceAbil, "Level")
            var masterAddValue = 0

            if (abilLevel == 100) {
                masterAddValue = 0.1
            }

            addAbilRate = 1 + (reinforceAbil.Level * 0.005 + masterAddValue);
            var hidden_abil_cls = GetClass("HiddenAbility_Reinforce", skill.ClassName);

            if (abilLevel >= 65  &&  hidden_abil_cls != null) {
                var hidden_abil_name = TryGetProp(hidden_abil_cls, "HiddenReinforceAbil");
                var hidden_abil = GetAbility(pc, hidden_abil_name);

                if (hidden_abil != null) {
                    var abil_level = TryGetProp(hidden_abil, "Level");
                    var add_factor = TryGetProp(hidden_abil_cls, "FactorByLevel", 0) * 0.01;
                    var add_value = 0;

                    if (abil_level == 10) {
                        add_value = TryGetProp(hidden_abil_cls, "AddFactor", 0) * 0.01
                    }

                    addAbilRate = addAbilRate * (1 + (abil_level * add_factor) + add_value);
                }

            }

        }

    }

    return addAbilRate
}

var value = TryGetProp(skill, 'Level', 1) * 2
value = value * SCR_REINFORCEABILITY_TOOLTIP(skill)
return value;
}
function Effect_CaptionRatio40201(level){
function SCR_REINFORCEABILITY_TOOLTIP(skill) {
    var addAbilRate = 1;

    if ("Priest11" != "None") {
        var reinforceAbil = GetAbility(pc, "Priest11")

        if (reinforceAbil != null) {
            var abilLevel = TryGetProp(reinforceAbil, "Level")
            var masterAddValue = 0

            if (abilLevel == 100) {
                masterAddValue = 0.1
            }

            addAbilRate = 1 + (reinforceAbil.Level * 0.005 + masterAddValue);
            var hidden_abil_cls = GetClass("HiddenAbility_Reinforce", skill.ClassName);

            if (abilLevel >= 65  &&  hidden_abil_cls != null) {
                var hidden_abil_name = TryGetProp(hidden_abil_cls, "HiddenReinforceAbil");
                var hidden_abil = GetAbility(pc, hidden_abil_name);

                if (hidden_abil != null) {
                    var abil_level = TryGetProp(hidden_abil, "Level");
                    var add_factor = TryGetProp(hidden_abil_cls, "FactorByLevel", 0) * 0.01;
                    var add_value = 0;

                    if (abil_level == 10) {
                        add_value = TryGetProp(hidden_abil_cls, "AddFactor", 0) * 0.01
                    }

                    addAbilRate = addAbilRate * (1 + (abil_level * add_factor) + add_value);
                }

            }

        }

    }

    return addAbilRate
}

var pcLevel = pc.Lv
var pcMNA = pc.MNA
var mnaRate = (pcMNA / (pcMNA + pcLevel) * 2) + 0.15
var skillValue = skill.Level
var value = skillValue * mnaRate
value = value * SCR_REINFORCEABILITY_TOOLTIP(skill)
return value
}
function Effect_CaptionRatio40203(level){
function SCR_REINFORCEABILITY_TOOLTIP(skill) {
    var addAbilRate = 1;

    if ("Priest13" != "None") {
        var reinforceAbil = GetAbility(pc, "Priest13")

        if (reinforceAbil != null) {
            var abilLevel = TryGetProp(reinforceAbil, "Level")
            var masterAddValue = 0

            if (abilLevel == 100) {
                masterAddValue = 0.1
            }

            addAbilRate = 1 + (reinforceAbil.Level * 0.005 + masterAddValue);
            var hidden_abil_cls = GetClass("HiddenAbility_Reinforce", skill.ClassName);

            if (abilLevel >= 65  &&  hidden_abil_cls != null) {
                var hidden_abil_name = TryGetProp(hidden_abil_cls, "HiddenReinforceAbil");
                var hidden_abil = GetAbility(pc, hidden_abil_name);

                if (hidden_abil != null) {
                    var abil_level = TryGetProp(hidden_abil, "Level");
                    var add_factor = TryGetProp(hidden_abil_cls, "FactorByLevel", 0) * 0.01;
                    var add_value = 0;

                    if (abil_level == 10) {
                        add_value = TryGetProp(hidden_abil_cls, "AddFactor", 0) * 0.01
                    }

                    addAbilRate = addAbilRate * (1 + (abil_level * add_factor) + add_value);
                }

            }

        }

    }

    return addAbilRate
}

var pcMNA = TryGetProp(pc, "MNA", 0)
var int = TryGetProp(pc, "INT", 0)
var mna_bonus = pcMNA * 1.5
var int_bonus = int * 1.5
var baseDamageValue = 150 + (skill.Level) * 150
var value = baseDamageValue + mna_bonus + int_bonus
value = value * SCR_REINFORCEABILITY_TOOLTIP(skill)
return Math.floor(value);
}
function Effect_CaptionRatio40204(level){
var value = skill.Level * 10
return value
}
function Effect_CaptionRatio40205(level){
function SCR_REINFORCEABILITY_TOOLTIP(skill) {
    var addAbilRate = 1;

    if ("Priest29" != "None") {
        var reinforceAbil = GetAbility(pc, "Priest29")

        if (reinforceAbil != null) {
            var abilLevel = TryGetProp(reinforceAbil, "Level")
            var masterAddValue = 0

            if (abilLevel == 100) {
                masterAddValue = 0.1
            }

            addAbilRate = 1 + (reinforceAbil.Level * 0.005 + masterAddValue);
            var hidden_abil_cls = GetClass("HiddenAbility_Reinforce", skill.ClassName);

            if (abilLevel >= 65  &&  hidden_abil_cls != null) {
                var hidden_abil_name = TryGetProp(hidden_abil_cls, "HiddenReinforceAbil");
                var hidden_abil = GetAbility(pc, hidden_abil_name);

                if (hidden_abil != null) {
                    var abil_level = TryGetProp(hidden_abil, "Level");
                    var add_factor = TryGetProp(hidden_abil_cls, "FactorByLevel", 0) * 0.01;
                    var add_value = 0;

                    if (abil_level == 10) {
                        add_value = TryGetProp(hidden_abil_cls, "AddFactor", 0) * 0.01
                    }

                    addAbilRate = addAbilRate * (1 + (abil_level * add_factor) + add_value);
                }

            }

        }

    }

    return addAbilRate
}

var pcMNA = pc.MNA
var mna_bonus = pcMNA * 2
var baseDamageValue = 100 + (skill.Level) * 100
var value = baseDamageValue + mna_bonus
value = value * SCR_REINFORCEABILITY_TOOLTIP(skill)
return Math.floor(value)
}
function Effect_CaptionRatio40206(level){
var value = 10 * skill.Level
return value
}
function Effect_CaptionRatio40209(){
return SCR_GET_MassHeal_Ratio_Common(skill)
}
function Effect_CaptionRatio40402(level){
var value = 1.5 * skill.Level
return value
}
function Effect_CaptionRatio40403(level){
var value = skill.Level * 2
return value
}
function Effect_CaptionRatio40404(level){
var value = skill.Level * 5
return value
}
function Effect_CaptionRatio40405(){
var value = 50;

if (IsPVPServer(pc) == 1) {
    value = 25;
}

return value
}
function Effect_CaptionRatio40406(level){
var value = 15 + skill.Level * 2
return value
}
function Effect_CaptionRatio40407(level){
var value = skill.Level * 3
return value
}
function Effect_CaptionRatio40501(level){
var value = 8 + skill.Level * 2
return value
}
function Effect_CaptionRatio40502(level){
var value = skill.Level * 2
return value
}
function Effect_CaptionRatio40506(level){
var value = 20 + (skill.Level * 5)
return Math.floor(value)
}
function Effect_CaptionRatio40508(level){
var value = 20 + (skill.Level * 5)
return Math.floor(value)
}
function Effect_CaptionRatio40602(level){
function SCR_REINFORCEABILITY_TOOLTIP(skill) {
    var addAbilRate = 1;

    if ("Paladin25" != "None") {
        var reinforceAbil = GetAbility(pc, "Paladin25")

        if (reinforceAbil != null) {
            var abilLevel = TryGetProp(reinforceAbil, "Level")
            var masterAddValue = 0

            if (abilLevel == 100) {
                masterAddValue = 0.1
            }

            addAbilRate = 1 + (reinforceAbil.Level * 0.005 + masterAddValue);
            var hidden_abil_cls = GetClass("HiddenAbility_Reinforce", skill.ClassName);

            if (abilLevel >= 65  &&  hidden_abil_cls != null) {
                var hidden_abil_name = TryGetProp(hidden_abil_cls, "HiddenReinforceAbil");
                var hidden_abil = GetAbility(pc, hidden_abil_name);

                if (hidden_abil != null) {
                    var abil_level = TryGetProp(hidden_abil, "Level");
                    var add_factor = TryGetProp(hidden_abil_cls, "FactorByLevel", 0) * 0.01;
                    var add_value = 0;

                    if (abil_level == 10) {
                        add_value = TryGetProp(hidden_abil_cls, "AddFactor", 0) * 0.01
                    }

                    addAbilRate = addAbilRate * (1 + (abil_level * add_factor) + add_value);
                }

            }

        }

    }

    return addAbilRate
}

var value = 107 + (skill.Level - 1) * 6.2
value = value * SCR_REINFORCEABILITY_TOOLTIP(skill)
return value
}
function Effect_CaptionRatio40603(level){
function SCR_REINFORCEABILITY_TOOLTIP(skill) {
    var addAbilRate = 1;

    if ("Paladin26" != "None") {
        var reinforceAbil = GetAbility(pc, "Paladin26")

        if (reinforceAbil != null) {
            var abilLevel = TryGetProp(reinforceAbil, "Level")
            var masterAddValue = 0

            if (abilLevel == 100) {
                masterAddValue = 0.1
            }

            addAbilRate = 1 + (reinforceAbil.Level * 0.005 + masterAddValue);
            var hidden_abil_cls = GetClass("HiddenAbility_Reinforce", skill.ClassName);

            if (abilLevel >= 65  &&  hidden_abil_cls != null) {
                var hidden_abil_name = TryGetProp(hidden_abil_cls, "HiddenReinforceAbil");
                var hidden_abil = GetAbility(pc, hidden_abil_name);

                if (hidden_abil != null) {
                    var abil_level = TryGetProp(hidden_abil, "Level");
                    var add_factor = TryGetProp(hidden_abil_cls, "FactorByLevel", 0) * 0.01;
                    var add_value = 0;

                    if (abil_level == 10) {
                        add_value = TryGetProp(hidden_abil_cls, "AddFactor", 0) * 0.01
                    }

                    addAbilRate = addAbilRate * (1 + (abil_level * add_factor) + add_value);
                }

            }

        }

    }

    return addAbilRate
}

var value = 10 + skill.Level * 2
value = value * SCR_REINFORCEABILITY_TOOLTIP(skill)
return value
}
function Effect_CaptionRatio40606(level){
var value = 10 * skill.Level
return value
}
function Effect_CaptionRatio40608(level){
function SCR_REINFORCEABILITY_TOOLTIP(skill) {
    var addAbilRate = 1;

    if ("Paladin27" != "None") {
        var reinforceAbil = GetAbility(pc, "Paladin27")

        if (reinforceAbil != null) {
            var abilLevel = TryGetProp(reinforceAbil, "Level")
            var masterAddValue = 0

            if (abilLevel == 100) {
                masterAddValue = 0.1
            }

            addAbilRate = 1 + (reinforceAbil.Level * 0.005 + masterAddValue);
            var hidden_abil_cls = GetClass("HiddenAbility_Reinforce", skill.ClassName);

            if (abilLevel >= 65  &&  hidden_abil_cls != null) {
                var hidden_abil_name = TryGetProp(hidden_abil_cls, "HiddenReinforceAbil");
                var hidden_abil = GetAbility(pc, hidden_abil_name);

                if (hidden_abil != null) {
                    var abil_level = TryGetProp(hidden_abil, "Level");
                    var add_factor = TryGetProp(hidden_abil_cls, "FactorByLevel", 0) * 0.01;
                    var add_value = 0;

                    if (abil_level == 10) {
                        add_value = TryGetProp(hidden_abil_cls, "AddFactor", 0) * 0.01
                    }

                    addAbilRate = addAbilRate * (1 + (abil_level * add_factor) + add_value);
                }

            }

        }

    }

    return addAbilRate
}

var value = 3 * skill.Level
var abil = GetAbility(pc, "Paladin40")

if (abil != null  &&  abil.ActiveState == 1) {
    value = 5 * skill.Level
}

value = value * SCR_REINFORCEABILITY_TOOLTIP(skill)
return value
}
function Effect_CaptionRatio40609(level){
var value = skill.Level * 2;
return value
}
function Effect_CaptionRatio40610(level){
function SCR_REINFORCEABILITY_TOOLTIP(skill) {
    var addAbilRate = 1;

    if ("Paladin24" != "None") {
        var reinforceAbil = GetAbility(pc, "Paladin24")

        if (reinforceAbil != null) {
            var abilLevel = TryGetProp(reinforceAbil, "Level")
            var masterAddValue = 0

            if (abilLevel == 100) {
                masterAddValue = 0.1
            }

            addAbilRate = 1 + (reinforceAbil.Level * 0.005 + masterAddValue);
            var hidden_abil_cls = GetClass("HiddenAbility_Reinforce", skill.ClassName);

            if (abilLevel >= 65  &&  hidden_abil_cls != null) {
                var hidden_abil_name = TryGetProp(hidden_abil_cls, "HiddenReinforceAbil");
                var hidden_abil = GetAbility(pc, hidden_abil_name);

                if (hidden_abil != null) {
                    var abil_level = TryGetProp(hidden_abil, "Level");
                    var add_factor = TryGetProp(hidden_abil_cls, "FactorByLevel", 0) * 0.01;
                    var add_value = 0;

                    if (abil_level == 10) {
                        add_value = TryGetProp(hidden_abil_cls, "AddFactor", 0) * 0.01
                    }

                    addAbilRate = addAbilRate * (1 + (abil_level * add_factor) + add_value);
                }

            }

        }

    }

    return addAbilRate
}

var value = skill.Level * 0.65
var abilPaladin33 = GetAbility(pc, "Paladin33")

if (abilPaladin33 != null  &&  TryGetProp(abilPaladin33, "ActiveState", 0) == 1) {
    value = skill.Level * 1.3
}

var abilPaladin34 = GetAbility(pc, "Paladin34")

if (abilPaladin34 != null  &&  TryGetProp(abilPaladin34, "ActiveState", 0) == 1) {
    value = skill.Level * 1.3
}

value = value * SCR_REINFORCEABILITY_TOOLTIP(skill)
return value
}
function Effect_CaptionRatio40701(level){
var value = skill.Level * 3
return value
}
function Effect_CaptionRatio40703(level){
var value = skill.Level
return Math.floor(value)
}
function Effect_CaptionRatio40708(level){
var value = 50 + 5 * (skill.Level-1);
return value
}
function Effect_CaptionRatio40802(level){
var value = 3 + skill.Level
return value
}
function Effect_CaptionRatio40803(level){
var value = 25 + skill.Level * 5
return value
}
function Effect_CaptionRatio40804(level){
var value = 100 * skill.Level
return value
}
function Effect_CaptionRatio40805(level){
var value = 9 * skill.Level
var abil = GetAbility(pc, "Pardoner4")

if (abil != null  &&  1 == abil.ActiveState) {
    value = value + (abil.Level * 3);
}

return value
}
function Effect_CaptionRatio40808(level){
function SCR_REINFORCEABILITY_TOOLTIP(skill) {
    var addAbilRate = 1;

    if ("Pardoner11" != "None") {
        var reinforceAbil = GetAbility(pc, "Pardoner11")

        if (reinforceAbil != null) {
            var abilLevel = TryGetProp(reinforceAbil, "Level")
            var masterAddValue = 0

            if (abilLevel == 100) {
                masterAddValue = 0.1
            }

            addAbilRate = 1 + (reinforceAbil.Level * 0.005 + masterAddValue);
            var hidden_abil_cls = GetClass("HiddenAbility_Reinforce", skill.ClassName);

            if (abilLevel >= 65  &&  hidden_abil_cls != null) {
                var hidden_abil_name = TryGetProp(hidden_abil_cls, "HiddenReinforceAbil");
                var hidden_abil = GetAbility(pc, hidden_abil_name);

                if (hidden_abil != null) {
                    var abil_level = TryGetProp(hidden_abil, "Level");
                    var add_factor = TryGetProp(hidden_abil_cls, "FactorByLevel", 0) * 0.01;
                    var add_value = 0;

                    if (abil_level == 10) {
                        add_value = TryGetProp(hidden_abil_cls, "AddFactor", 0) * 0.01
                    }

                    addAbilRate = addAbilRate * (1 + (abil_level * add_factor) + add_value);
                }

            }

        }

    }

    return addAbilRate
}

var value = skill.Level * 1.5
var pcStat = TryGetProp(pc, "MNA", 1)
var pcLevel = TryGetProp(pc, "Lv", 1)
var casterMnaRate = (pcStat / (pcStat + pcLevel) * 2) + 0.15
value = value * casterMnaRate
value = value * SCR_REINFORCEABILITY_TOOLTIP(skill)
return value
}
function Effect_CaptionRatio40901(level){
var value = 10 + skill.Level * 1
return value
}
function Effect_CaptionRatio40902(level){
var value = 1 + ((skill.Level * 1) / 2)
return Math.ceil(value)
}
function Effect_CaptionRatio40905(level){
function SCR_REINFORCEABILITY_TOOLTIP(skill) {
    var addAbilRate = 1;

    if ("Druid11" != "None") {
        var reinforceAbil = GetAbility(pc, "Druid11")

        if (reinforceAbil != null) {
            var abilLevel = TryGetProp(reinforceAbil, "Level")
            var masterAddValue = 0

            if (abilLevel == 100) {
                masterAddValue = 0.1
            }

            addAbilRate = 1 + (reinforceAbil.Level * 0.005 + masterAddValue);
            var hidden_abil_cls = GetClass("HiddenAbility_Reinforce", skill.ClassName);

            if (abilLevel >= 65  &&  hidden_abil_cls != null) {
                var hidden_abil_name = TryGetProp(hidden_abil_cls, "HiddenReinforceAbil");
                var hidden_abil = GetAbility(pc, hidden_abil_name);

                if (hidden_abil != null) {
                    var abil_level = TryGetProp(hidden_abil, "Level");
                    var add_factor = TryGetProp(hidden_abil_cls, "FactorByLevel", 0) * 0.01;
                    var add_value = 0;

                    if (abil_level == 10) {
                        add_value = TryGetProp(hidden_abil_cls, "AddFactor", 0) * 0.01
                    }

                    addAbilRate = addAbilRate * (1 + (abil_level * add_factor) + add_value);
                }

            }

        }

    }

    return addAbilRate
}

var value = skill.Level * 7
value = value * SCR_REINFORCEABILITY_TOOLTIP(skill)
return value
}
function Effect_CaptionRatio40906(level){
var value = 41 + (7.6 * (skill.Level - 1));
return value
}
function Effect_CaptionRatio40908(level){
var value = skill.Level * 10
return value;
}
function Effect_CaptionRatio40910(){
var value = 5

if (IsPVPField(pc) == 1  &&  value > 2) {
    value = Math.floor((Math.pow(Math.max(0, value-2), 0.5)))+Math.min(2, value)
}

return value
}
function Effect_CaptionRatio41001(level){
var value = 1 + skill.Level * 2;
return value
}
function Effect_CaptionRatio41003(level){
var value = skill.Level;
return value
}
function Effect_CaptionRatio41005(level){
function SCR_REINFORCEABILITY_TOOLTIP(skill) {
    var addAbilRate = 1;

    if ("Oracle15" != "None") {
        var reinforceAbil = GetAbility(pc, "Oracle15")

        if (reinforceAbil != null) {
            var abilLevel = TryGetProp(reinforceAbil, "Level")
            var masterAddValue = 0

            if (abilLevel == 100) {
                masterAddValue = 0.1
            }

            addAbilRate = 1 + (reinforceAbil.Level * 0.005 + masterAddValue);
            var hidden_abil_cls = GetClass("HiddenAbility_Reinforce", skill.ClassName);

            if (abilLevel >= 65  &&  hidden_abil_cls != null) {
                var hidden_abil_name = TryGetProp(hidden_abil_cls, "HiddenReinforceAbil");
                var hidden_abil = GetAbility(pc, hidden_abil_name);

                if (hidden_abil != null) {
                    var abil_level = TryGetProp(hidden_abil, "Level");
                    var add_factor = TryGetProp(hidden_abil_cls, "FactorByLevel", 0) * 0.01;
                    var add_value = 0;

                    if (abil_level == 10) {
                        add_value = TryGetProp(hidden_abil_cls, "AddFactor", 0) * 0.01
                    }

                    addAbilRate = addAbilRate * (1 + (abil_level * add_factor) + add_value);
                }

            }

        }

    }

    return addAbilRate
}

var value = 5 + skill.Level * 2;
value = value * SCR_REINFORCEABILITY_TOOLTIP(skill);
return Math.floor(value);
}
function Effect_CaptionRatio41006(){
var value = 300;
var Oracle3_abil = GetAbility(pc, "Oracle3")

if (Oracle3_abil != null  &&  1 == Oracle3_abil.ActiveState) {
    value = value + Oracle3_abil.Level * 60;
}

return value
}
function Effect_CaptionRatio41008(level){
function SCR_REINFORCEABILITY_TOOLTIP(skill) {
    var addAbilRate = 1;

    if ("Oracle19" != "None") {
        var reinforceAbil = GetAbility(pc, "Oracle19")

        if (reinforceAbil != null) {
            var abilLevel = TryGetProp(reinforceAbil, "Level")
            var masterAddValue = 0

            if (abilLevel == 100) {
                masterAddValue = 0.1
            }

            addAbilRate = 1 + (reinforceAbil.Level * 0.005 + masterAddValue);
            var hidden_abil_cls = GetClass("HiddenAbility_Reinforce", skill.ClassName);

            if (abilLevel >= 65  &&  hidden_abil_cls != null) {
                var hidden_abil_name = TryGetProp(hidden_abil_cls, "HiddenReinforceAbil");
                var hidden_abil = GetAbility(pc, hidden_abil_name);

                if (hidden_abil != null) {
                    var abil_level = TryGetProp(hidden_abil, "Level");
                    var add_factor = TryGetProp(hidden_abil_cls, "FactorByLevel", 0) * 0.01;
                    var add_value = 0;

                    if (abil_level == 10) {
                        add_value = TryGetProp(hidden_abil_cls, "AddFactor", 0) * 0.01
                    }

                    addAbilRate = addAbilRate * (1 + (abil_level * add_factor) + add_value);
                }

            }

        }

    }

    return addAbilRate
}

var value = skill.Level * 5
value = value * SCR_REINFORCEABILITY_TOOLTIP(skill);
return value;
}
function Effect_CaptionRatio41011(level){
function SCR_REINFORCEABILITY_TOOLTIP(skill) {
    var addAbilRate = 1;

    if ("Oracle22" != "None") {
        var reinforceAbil = GetAbility(pc, "Oracle22")

        if (reinforceAbil != null) {
            var abilLevel = TryGetProp(reinforceAbil, "Level")
            var masterAddValue = 0

            if (abilLevel == 100) {
                masterAddValue = 0.1
            }

            addAbilRate = 1 + (reinforceAbil.Level * 0.005 + masterAddValue);
            var hidden_abil_cls = GetClass("HiddenAbility_Reinforce", skill.ClassName);

            if (abilLevel >= 65  &&  hidden_abil_cls != null) {
                var hidden_abil_name = TryGetProp(hidden_abil_cls, "HiddenReinforceAbil");
                var hidden_abil = GetAbility(pc, hidden_abil_name);

                if (hidden_abil != null) {
                    var abil_level = TryGetProp(hidden_abil, "Level");
                    var add_factor = TryGetProp(hidden_abil_cls, "FactorByLevel", 0) * 0.01;
                    var add_value = 0;

                    if (abil_level == 10) {
                        add_value = TryGetProp(hidden_abil_cls, "AddFactor", 0) * 0.01
                    }

                    addAbilRate = addAbilRate * (1 + (abil_level * add_factor) + add_value);
                }

            }

        }

    }

    return addAbilRate
}

var value = skill.Level * 6
value = value * SCR_REINFORCEABILITY_TOOLTIP(skill);
return value
}
function Effect_CaptionRatio41012(level){
var value = (skill.Level * 8) - 7
return value
}
function Effect_CaptionRatio41101(level){
var value = 1020 + (skill.Level - 1) * 137.5
return Math.floor(value);
}
function Effect_CaptionRatio41102(){
var value = 4

if (IsPVPField(pc) == 1  &&  value > 2) {
    value = Math.floor((Math.pow(Math.max(0, value-2), 0.5)))+Math.min(2, value)
}

return value
}
function Effect_CaptionRatio41103(level){
var value = 6 - skill.Level

if (value <= 0) {
    value = 1
}

return value;
}
function Effect_CaptionRatio41105(level){
var value = 3 + skill.Level * 2
return value;
}
function Effect_CaptionRatio41107(level){
var value = skill.Level * 2
return value
}
function Effect_CaptionRatio41108(level){
var value = Math.min(skill.Level * 10, 100)
return value;
}
function Effect_CaptionRatio41109(level){
var value = 20 - (skill.Level * 2)
return value;
}
function Effect_CaptionRatio41110(level){
function SCR_REINFORCEABILITY_TOOLTIP(skill) {
    var addAbilRate = 1;

    if ("PlagueDoctor17" != "None") {
        var reinforceAbil = GetAbility(pc, "PlagueDoctor17")

        if (reinforceAbil != null) {
            var abilLevel = TryGetProp(reinforceAbil, "Level")
            var masterAddValue = 0

            if (abilLevel == 100) {
                masterAddValue = 0.1
            }

            addAbilRate = 1 + (reinforceAbil.Level * 0.005 + masterAddValue);
            var hidden_abil_cls = GetClass("HiddenAbility_Reinforce", skill.ClassName);

            if (abilLevel >= 65  &&  hidden_abil_cls != null) {
                var hidden_abil_name = TryGetProp(hidden_abil_cls, "HiddenReinforceAbil");
                var hidden_abil = GetAbility(pc, hidden_abil_name);

                if (hidden_abil != null) {
                    var abil_level = TryGetProp(hidden_abil, "Level");
                    var add_factor = TryGetProp(hidden_abil_cls, "FactorByLevel", 0) * 0.01;
                    var add_value = 0;

                    if (abil_level == 10) {
                        add_value = TryGetProp(hidden_abil_cls, "AddFactor", 0) * 0.01
                    }

                    addAbilRate = addAbilRate * (1 + (abil_level * add_factor) + add_value);
                }

            }

        }

    }

    return addAbilRate
}

var value = 3 + skill.Level * 0.5;
value = value * SCR_REINFORCEABILITY_TOOLTIP(skill)
var casterMNA = pc.MNA;
var baseLv = pc.Lv;
var addRate = casterMNA / baseLv;

if (addRate <= 0) {
    addRate = 0;
} else if (addRate >= 1) {
    addRate = 1;
}

value = Math.floor(value * (1 + addRate));
return value;
}
function Effect_CaptionRatio41201(level){
var value = 3.5 * skill.Level
return value
}
function Effect_CaptionRatio41203(){
function SCR_REINFORCEABILITY_TOOLTIP(skill) {
    var addAbilRate = 1;

    if ("Kabbalist26" != "None") {
        var reinforceAbil = GetAbility(pc, "Kabbalist26")

        if (reinforceAbil != null) {
            var abilLevel = TryGetProp(reinforceAbil, "Level")
            var masterAddValue = 0

            if (abilLevel == 100) {
                masterAddValue = 0.1
            }

            addAbilRate = 1 + (reinforceAbil.Level * 0.005 + masterAddValue);
            var hidden_abil_cls = GetClass("HiddenAbility_Reinforce", skill.ClassName);

            if (abilLevel >= 65  &&  hidden_abil_cls != null) {
                var hidden_abil_name = TryGetProp(hidden_abil_cls, "HiddenReinforceAbil");
                var hidden_abil = GetAbility(pc, hidden_abil_name);

                if (hidden_abil != null) {
                    var abil_level = TryGetProp(hidden_abil, "Level");
                    var add_factor = TryGetProp(hidden_abil_cls, "FactorByLevel", 0) * 0.01;
                    var add_value = 0;

                    if (abil_level == 10) {
                        add_value = TryGetProp(hidden_abil_cls, "AddFactor", 0) * 0.01
                    }

                    addAbilRate = addAbilRate * (1 + (abil_level * add_factor) + add_value);
                }

            }

        }

    }

    return addAbilRate
}

var value = 30
value = value * SCR_REINFORCEABILITY_TOOLTIP(skill)
var Kabbalist23_Abil = GetAbility(pc, "Kabbalist23")

if (Kabbalist23_Abil != null  &&  TryGetProp(Kabbalist23_Abil, "ActiveState", 0) == 1) {
    value = value * 0.5
}

return value
}
function Effect_CaptionRatio41204(level){
var value = skill.Level * 3
return value
}
function Effect_CaptionRatio41205(){
var value = 10;
var abilKabbalist14 = GetAbility(pc, "Kabbalist14");

if (abilKabbalist14 != null  &&  abilKabbalist14.ActiveState == 1) {
    value = value + abilKabbalist14.Level;
}

return value;
}
function Effect_CaptionRatio41206(){
var value = 10;
var abilKabbalist14 = GetAbility(pc, "Kabbalist14");

if (abilKabbalist14 != null  &&  abilKabbalist14.ActiveState == 1) {
    value = value + abilKabbalist14.Level;
}

return value;
}
function Effect_CaptionRatio41207(level){
var value = skill.Level * 8
return value
}
function Effect_CaptionRatio41208(level){
var value = skill.Level
return value
}
function Effect_CaptionRatio41211(level){
function SCR_REINFORCEABILITY_TOOLTIP(skill) {
    var addAbilRate = 1;

    if ("Kabbalist25" != "None") {
        var reinforceAbil = GetAbility(pc, "Kabbalist25")

        if (reinforceAbil != null) {
            var abilLevel = TryGetProp(reinforceAbil, "Level")
            var masterAddValue = 0

            if (abilLevel == 100) {
                masterAddValue = 0.1
            }

            addAbilRate = 1 + (reinforceAbil.Level * 0.005 + masterAddValue);
            var hidden_abil_cls = GetClass("HiddenAbility_Reinforce", skill.ClassName);

            if (abilLevel >= 65  &&  hidden_abil_cls != null) {
                var hidden_abil_name = TryGetProp(hidden_abil_cls, "HiddenReinforceAbil");
                var hidden_abil = GetAbility(pc, hidden_abil_name);

                if (hidden_abil != null) {
                    var abil_level = TryGetProp(hidden_abil, "Level");
                    var add_factor = TryGetProp(hidden_abil_cls, "FactorByLevel", 0) * 0.01;
                    var add_value = 0;

                    if (abil_level == 10) {
                        add_value = TryGetProp(hidden_abil_cls, "AddFactor", 0) * 0.01
                    }

                    addAbilRate = addAbilRate * (1 + (abil_level * add_factor) + add_value);
                }

            }

        }

    }

    return addAbilRate
}

var value = 45 + (skill.Level - 1) * 21.1
value = Math.floor(value * SCR_REINFORCEABILITY_TOOLTIP(skill))
return value
}
function Effect_CaptionRatio41301(level){
function SCR_REINFORCEABILITY_TOOLTIP(skill) {
    var addAbilRate = 1;

    if ("Chaplain13" != "None") {
        var reinforceAbil = GetAbility(pc, "Chaplain13")

        if (reinforceAbil != null) {
            var abilLevel = TryGetProp(reinforceAbil, "Level")
            var masterAddValue = 0

            if (abilLevel == 100) {
                masterAddValue = 0.1
            }

            addAbilRate = 1 + (reinforceAbil.Level * 0.005 + masterAddValue);
            var hidden_abil_cls = GetClass("HiddenAbility_Reinforce", skill.ClassName);

            if (abilLevel >= 65  &&  hidden_abil_cls != null) {
                var hidden_abil_name = TryGetProp(hidden_abil_cls, "HiddenReinforceAbil");
                var hidden_abil = GetAbility(pc, hidden_abil_name);

                if (hidden_abil != null) {
                    var abil_level = TryGetProp(hidden_abil, "Level");
                    var add_factor = TryGetProp(hidden_abil_cls, "FactorByLevel", 0) * 0.01;
                    var add_value = 0;

                    if (abil_level == 10) {
                        add_value = TryGetProp(hidden_abil_cls, "AddFactor", 0) * 0.01
                    }

                    addAbilRate = addAbilRate * (1 + (abil_level * add_factor) + add_value);
                }

            }

        }

    }

    return addAbilRate
}

var value = (8 + skill.Level * 0.5)
value = value * SCR_REINFORCEABILITY_TOOLTIP(skill)
return value
}
function Effect_CaptionRatio41302(){
var value = 30
return value
}
function Effect_CaptionRatio41306(level){
var value = skill.Level * 5
return value
}
function Effect_CaptionRatio41406(){
var value = 0
var abil = GetAbility(pc, "Inquisitor8")

if (abil != null  &&  abil.ActiveState == 1) {
    value = 15
    var abilInquisitor20 = GetAbility(pc, "Inquisitor20")

    if (abilInquisitor20 != null  &&  abilInquisitor20.ActiveState == 1) {
        value = value + abilInquisitor20.Level
    }

}

return value
}
function Effect_CaptionRatio41409(level){
var value = 10 + skill.Level * 2
return value
}
function Effect_CaptionRatio41410(){
var value = 5
var STR = pc.STR
var strValue = STR / 50

if (strValue <= 0) {
    strValue = 0
}

value = value + strValue

if (IsPVPField(pc) == 1  &&  value > 2) {
    value = Math.floor((Math.pow(Math.max(0, value-2), 0.5)))+Math.min(2, value)
}

return Math.floor(value)
}
function Effect_CaptionRatio41602(level){
var value = 5 + skill.Level
return Math.floor(value)
}
function Effect_CaptionRatio41603(level){
var value = skill.Level * 2
return value
}
function Effect_CaptionRatio41604(level){
var value = skill.Level * 5
return value;
}
function Effect_CaptionRatio41606(level){
var value = 15 + (5 * skill.Level)
return Math.floor(value)
}
function Effect_CaptionRatio41701(level){
var value = 15 + (skill.Level-1) * 2.5
return value
}
function Effect_CaptionRatio41702(){
var value = 0
var abil = GetAbility(pc, "Zealot4")

if (abil != null  &&  abil.ActiveState == 1) {
    value = abil.Level * 300
}

return value
}
function Effect_CaptionRatio41703(level){
var value = 15 + skill.Level * 2
return value
}
function Effect_CaptionRatio41704(level){
var value = 20 + skill.Level * 4
return value
}
function Effect_CaptionRatio41705(){
var basicSP = 25;
var decsp = 0;
var bylvCorrect = 0

if (basicSP == 0) {
    return 0;
}

var lv = pc.Lv
bylvCorrect = lv - 300

if (bylvCorrect < 0) {
    bylvCorrect = bylvCorrect * 2.75 / 1000
} else if (bylvCorrect >= 0) {
    bylvCorrect = bylvCorrect * 1.25 / 1000
}

var value = basicSP * (1 + bylvCorrect)
var abilAddSP = 0 // @rjgtav. Attributes aren't supported yet;
abilAddSP = abilAddSP / 100;

if (IsBuffApplied(pc, 'Wizard_Wild_buff') == 'YES') {
    value = value * 1.5;
    return Math.floor(value);
}


if (IsBuffApplied(pc, 'MalleusMaleficarum_Debuff') == 'YES') {
    value = value * 2
    return Math.floor(value);
}

value = value + (value * abilAddSP);
var zeminaLv = GetExProp(pc, "ZEMINA_BUFF_LV");

if (zeminaLv > 0) {
    decsp = 4 + (zeminaLv * 4);
}

value = value - decsp;

if (value < 1) {
    value = 0
}

return Math.floor(value);
}
function Effect_CaptionRatio41706(level){
var value = 20 + ((skill.Level - 1) * 20)
return value
}
function Effect_CaptionRatio41707(level){
return 15 + skill.Level*2;
}
function Effect_CaptionRatio41801(){
var value = 5;
var abilExorcist2 = GetAbility(pc, "Exorcist2");

if (abilExorcist2 != null  &&  TryGetProp(abilExorcist2, "ActiveState") == 1) {
    value = value + abilExorcist2.Level;
}


if (IsPVPField(pc) == 1  &&  value > 2) {
    value = Math.floor((Math.pow(Math.max(0, value-2), 0.5)))+Math.min(2, value)
}

return value;
}
function Effect_CaptionRatio41803(){
var value = 10

if (IsPVPField(pc) == 1  &&  value > 2) {
    value = Math.floor((Math.pow(Math.max(0, value-2), 0.5)))+Math.min(2, value)
}

return value
}
function Effect_CaptionRatio41804(level){
return skill.Level * 5
}
function Effect_CaptionRatio41901(level){
function SCR_REINFORCEABILITY_TOOLTIP(skill) {
    var addAbilRate = 1;

    if ("Crusader3" != "None") {
        var reinforceAbil = GetAbility(pc, "Crusader3")

        if (reinforceAbil != null) {
            var abilLevel = TryGetProp(reinforceAbil, "Level")
            var masterAddValue = 0

            if (abilLevel == 100) {
                masterAddValue = 0.1
            }

            addAbilRate = 1 + (reinforceAbil.Level * 0.005 + masterAddValue);
            var hidden_abil_cls = GetClass("HiddenAbility_Reinforce", skill.ClassName);

            if (abilLevel >= 65  &&  hidden_abil_cls != null) {
                var hidden_abil_name = TryGetProp(hidden_abil_cls, "HiddenReinforceAbil");
                var hidden_abil = GetAbility(pc, hidden_abil_name);

                if (hidden_abil != null) {
                    var abil_level = TryGetProp(hidden_abil, "Level");
                    var add_factor = TryGetProp(hidden_abil_cls, "FactorByLevel", 0) * 0.01;
                    var add_value = 0;

                    if (abil_level == 10) {
                        add_value = TryGetProp(hidden_abil_cls, "AddFactor", 0) * 0.01
                    }

                    addAbilRate = addAbilRate * (1 + (abil_level * add_factor) + add_value);
                }

            }

        }

    }

    return addAbilRate
}

var value = (16 + (skill.Level - 1) * 2.7) * 0.4
value = Math.floor(value * SCR_REINFORCEABILITY_TOOLTIP(skill))
return Math.floor(value)
}
function Effect_CaptionRatio41902(level){
function SCR_REINFORCEABILITY_TOOLTIP(skill) {
    var addAbilRate = 1;

    if ("Crusader4" != "None") {
        var reinforceAbil = GetAbility(pc, "Crusader4")

        if (reinforceAbil != null) {
            var abilLevel = TryGetProp(reinforceAbil, "Level")
            var masterAddValue = 0

            if (abilLevel == 100) {
                masterAddValue = 0.1
            }

            addAbilRate = 1 + (reinforceAbil.Level * 0.005 + masterAddValue);
            var hidden_abil_cls = GetClass("HiddenAbility_Reinforce", skill.ClassName);

            if (abilLevel >= 65  &&  hidden_abil_cls != null) {
                var hidden_abil_name = TryGetProp(hidden_abil_cls, "HiddenReinforceAbil");
                var hidden_abil = GetAbility(pc, hidden_abil_name);

                if (hidden_abil != null) {
                    var abil_level = TryGetProp(hidden_abil, "Level");
                    var add_factor = TryGetProp(hidden_abil_cls, "FactorByLevel", 0) * 0.01;
                    var add_value = 0;

                    if (abil_level == 10) {
                        add_value = TryGetProp(hidden_abil_cls, "AddFactor", 0) * 0.01
                    }

                    addAbilRate = addAbilRate * (1 + (abil_level * add_factor) + add_value);
                }

            }

        }

    }

    return addAbilRate
}

var value = (67 + (skill.Level - 1) * 67.3) * 0.4
value = Math.floor(value * SCR_REINFORCEABILITY_TOOLTIP(skill))
return Math.floor(value)
}
function Effect_CaptionRatio41903(level){
function SCR_REINFORCEABILITY_TOOLTIP(skill) {
    var addAbilRate = 1;

    if ("Crusader12" != "None") {
        var reinforceAbil = GetAbility(pc, "Crusader12")

        if (reinforceAbil != null) {
            var abilLevel = TryGetProp(reinforceAbil, "Level")
            var masterAddValue = 0

            if (abilLevel == 100) {
                masterAddValue = 0.1
            }

            addAbilRate = 1 + (reinforceAbil.Level * 0.005 + masterAddValue);
            var hidden_abil_cls = GetClass("HiddenAbility_Reinforce", skill.ClassName);

            if (abilLevel >= 65  &&  hidden_abil_cls != null) {
                var hidden_abil_name = TryGetProp(hidden_abil_cls, "HiddenReinforceAbil");
                var hidden_abil = GetAbility(pc, hidden_abil_name);

                if (hidden_abil != null) {
                    var abil_level = TryGetProp(hidden_abil, "Level");
                    var add_factor = TryGetProp(hidden_abil_cls, "FactorByLevel", 0) * 0.01;
                    var add_value = 0;

                    if (abil_level == 10) {
                        add_value = TryGetProp(hidden_abil_cls, "AddFactor", 0) * 0.01
                    }

                    addAbilRate = addAbilRate * (1 + (abil_level * add_factor) + add_value);
                }

            }

        }

    }

    return addAbilRate
}

var value = (10 + (skill.Level - 1) * 2.7) * 0.4
value = Math.floor(value * SCR_REINFORCEABILITY_TOOLTIP(skill))
return Math.floor(value)
}
function Effect_CaptionRatio41905(level){
function SCR_REINFORCEABILITY_TOOLTIP(skill) {
    var addAbilRate = 1;

    if ("Crusader5" != "None") {
        var reinforceAbil = GetAbility(pc, "Crusader5")

        if (reinforceAbil != null) {
            var abilLevel = TryGetProp(reinforceAbil, "Level")
            var masterAddValue = 0

            if (abilLevel == 100) {
                masterAddValue = 0.1
            }

            addAbilRate = 1 + (reinforceAbil.Level * 0.005 + masterAddValue);
            var hidden_abil_cls = GetClass("HiddenAbility_Reinforce", skill.ClassName);

            if (abilLevel >= 65  &&  hidden_abil_cls != null) {
                var hidden_abil_name = TryGetProp(hidden_abil_cls, "HiddenReinforceAbil");
                var hidden_abil = GetAbility(pc, hidden_abil_name);

                if (hidden_abil != null) {
                    var abil_level = TryGetProp(hidden_abil, "Level");
                    var add_factor = TryGetProp(hidden_abil_cls, "FactorByLevel", 0) * 0.01;
                    var add_value = 0;

                    if (abil_level == 10) {
                        add_value = TryGetProp(hidden_abil_cls, "AddFactor", 0) * 0.01
                    }

                    addAbilRate = addAbilRate * (1 + (abil_level * add_factor) + add_value);
                }

            }

        }

    }

    return addAbilRate
}

var value = (76 + (skill.Level - 1) * 20) * 0.4
value = Math.floor(value * SCR_REINFORCEABILITY_TOOLTIP(skill))
return Math.floor(value)
}
function Effect_CaptionRatio41906(level){
function SCR_REINFORCEABILITY_TOOLTIP(skill) {
    var addAbilRate = 1;

    if ("Crusader6" != "None") {
        var reinforceAbil = GetAbility(pc, "Crusader6")

        if (reinforceAbil != null) {
            var abilLevel = TryGetProp(reinforceAbil, "Level")
            var masterAddValue = 0

            if (abilLevel == 100) {
                masterAddValue = 0.1
            }

            addAbilRate = 1 + (reinforceAbil.Level * 0.005 + masterAddValue);
            var hidden_abil_cls = GetClass("HiddenAbility_Reinforce", skill.ClassName);

            if (abilLevel >= 65  &&  hidden_abil_cls != null) {
                var hidden_abil_name = TryGetProp(hidden_abil_cls, "HiddenReinforceAbil");
                var hidden_abil = GetAbility(pc, hidden_abil_name);

                if (hidden_abil != null) {
                    var abil_level = TryGetProp(hidden_abil, "Level");
                    var add_factor = TryGetProp(hidden_abil_cls, "FactorByLevel", 0) * 0.01;
                    var add_value = 0;

                    if (abil_level == 10) {
                        add_value = TryGetProp(hidden_abil_cls, "AddFactor", 0) * 0.01
                    }

                    addAbilRate = addAbilRate * (1 + (abil_level * add_factor) + add_value);
                }

            }

        }

    }

    return addAbilRate
}

var value = (14 + (skill.Level - 1) * 3.7) * 0.4
value = Math.floor(value * SCR_REINFORCEABILITY_TOOLTIP(skill))
return Math.floor(value)
}
function Effect_CaptionRatio41907(level){
function SCR_REINFORCEABILITY_TOOLTIP(skill) {
    var addAbilRate = 1;

    if ("Crusader11" != "None") {
        var reinforceAbil = GetAbility(pc, "Crusader11")

        if (reinforceAbil != null) {
            var abilLevel = TryGetProp(reinforceAbil, "Level")
            var masterAddValue = 0

            if (abilLevel == 100) {
                masterAddValue = 0.1
            }

            addAbilRate = 1 + (reinforceAbil.Level * 0.005 + masterAddValue);
            var hidden_abil_cls = GetClass("HiddenAbility_Reinforce", skill.ClassName);

            if (abilLevel >= 65  &&  hidden_abil_cls != null) {
                var hidden_abil_name = TryGetProp(hidden_abil_cls, "HiddenReinforceAbil");
                var hidden_abil = GetAbility(pc, hidden_abil_name);

                if (hidden_abil != null) {
                    var abil_level = TryGetProp(hidden_abil, "Level");
                    var add_factor = TryGetProp(hidden_abil_cls, "FactorByLevel", 0) * 0.01;
                    var add_value = 0;

                    if (abil_level == 10) {
                        add_value = TryGetProp(hidden_abil_cls, "AddFactor", 0) * 0.01
                    }

                    addAbilRate = addAbilRate * (1 + (abil_level * add_factor) + add_value);
                }

            }

        }

    }

    return addAbilRate
}

var value = (42 + (skill.Level - 1) * 7.1) * 0.4
value = Math.floor(value * SCR_REINFORCEABILITY_TOOLTIP(skill))
return Math.floor(value)
}
function Effect_CaptionRatio50001(level){
function SCR_REINFORCEABILITY_TOOLTIP(skill) {
    var addAbilRate = 1;

    if ("Scout18" != "None") {
        var reinforceAbil = GetAbility(pc, "Scout18")

        if (reinforceAbil != null) {
            var abilLevel = TryGetProp(reinforceAbil, "Level")
            var masterAddValue = 0

            if (abilLevel == 100) {
                masterAddValue = 0.1
            }

            addAbilRate = 1 + (reinforceAbil.Level * 0.005 + masterAddValue);
            var hidden_abil_cls = GetClass("HiddenAbility_Reinforce", skill.ClassName);

            if (abilLevel >= 65  &&  hidden_abil_cls != null) {
                var hidden_abil_name = TryGetProp(hidden_abil_cls, "HiddenReinforceAbil");
                var hidden_abil = GetAbility(pc, hidden_abil_name);

                if (hidden_abil != null) {
                    var abil_level = TryGetProp(hidden_abil, "Level");
                    var add_factor = TryGetProp(hidden_abil_cls, "FactorByLevel", 0) * 0.01;
                    var add_value = 0;

                    if (abil_level == 10) {
                        add_value = TryGetProp(hidden_abil_cls, "AddFactor", 0) * 0.01
                    }

                    addAbilRate = addAbilRate * (1 + (abil_level * add_factor) + add_value);
                }

            }

        }

    }

    return addAbilRate
}

var value = 23 + skill.Level * 2;
value = Math.floor(value * SCR_REINFORCEABILITY_TOOLTIP(skill))
return value
}
function Effect_CaptionRatio50004(level){
function SCR_REINFORCEABILITY_TOOLTIP(skill) {
    var addAbilRate = 1;

    if ("Scout21" != "None") {
        var reinforceAbil = GetAbility(pc, "Scout21")

        if (reinforceAbil != null) {
            var abilLevel = TryGetProp(reinforceAbil, "Level")
            var masterAddValue = 0

            if (abilLevel == 100) {
                masterAddValue = 0.1
            }

            addAbilRate = 1 + (reinforceAbil.Level * 0.005 + masterAddValue);
            var hidden_abil_cls = GetClass("HiddenAbility_Reinforce", skill.ClassName);

            if (abilLevel >= 65  &&  hidden_abil_cls != null) {
                var hidden_abil_name = TryGetProp(hidden_abil_cls, "HiddenReinforceAbil");
                var hidden_abil = GetAbility(pc, hidden_abil_name);

                if (hidden_abil != null) {
                    var abil_level = TryGetProp(hidden_abil, "Level");
                    var add_factor = TryGetProp(hidden_abil_cls, "FactorByLevel", 0) * 0.01;
                    var add_value = 0;

                    if (abil_level == 10) {
                        add_value = TryGetProp(hidden_abil_cls, "AddFactor", 0) * 0.01
                    }

                    addAbilRate = addAbilRate * (1 + (abil_level * add_factor) + add_value);
                }

            }

        }

    }

    return addAbilRate
}

var value = skill.Level * 5
value = value * SCR_REINFORCEABILITY_TOOLTIP(skill)
return value
}
function Effect_CaptionRatio50005(level){
function SCR_REINFORCEABILITY_TOOLTIP(skill) {
    var addAbilRate = 1;

    if ("Scout22" != "None") {
        var reinforceAbil = GetAbility(pc, "Scout22")

        if (reinforceAbil != null) {
            var abilLevel = TryGetProp(reinforceAbil, "Level")
            var masterAddValue = 0

            if (abilLevel == 100) {
                masterAddValue = 0.1
            }

            addAbilRate = 1 + (reinforceAbil.Level * 0.005 + masterAddValue);
            var hidden_abil_cls = GetClass("HiddenAbility_Reinforce", skill.ClassName);

            if (abilLevel >= 65  &&  hidden_abil_cls != null) {
                var hidden_abil_name = TryGetProp(hidden_abil_cls, "HiddenReinforceAbil");
                var hidden_abil = GetAbility(pc, hidden_abil_name);

                if (hidden_abil != null) {
                    var abil_level = TryGetProp(hidden_abil, "Level");
                    var add_factor = TryGetProp(hidden_abil_cls, "FactorByLevel", 0) * 0.01;
                    var add_value = 0;

                    if (abil_level == 10) {
                        add_value = TryGetProp(hidden_abil_cls, "AddFactor", 0) * 0.01
                    }

                    addAbilRate = addAbilRate * (1 + (abil_level * add_factor) + add_value);
                }

            }

        }

    }

    return addAbilRate
}

var value = skill.Level * 4
value = Math.floor(value * SCR_REINFORCEABILITY_TOOLTIP(skill))
return value
}
function Effect_CaptionRatio50101(level){
function SCR_REINFORCEABILITY_TOOLTIP(skill) {
    var addAbilRate = 1;

    if ("Assassin1" != "None") {
        var reinforceAbil = GetAbility(pc, "Assassin1")

        if (reinforceAbil != null) {
            var abilLevel = TryGetProp(reinforceAbil, "Level")
            var masterAddValue = 0

            if (abilLevel == 100) {
                masterAddValue = 0.1
            }

            addAbilRate = 1 + (reinforceAbil.Level * 0.005 + masterAddValue);
            var hidden_abil_cls = GetClass("HiddenAbility_Reinforce", skill.ClassName);

            if (abilLevel >= 65  &&  hidden_abil_cls != null) {
                var hidden_abil_name = TryGetProp(hidden_abil_cls, "HiddenReinforceAbil");
                var hidden_abil = GetAbility(pc, hidden_abil_name);

                if (hidden_abil != null) {
                    var abil_level = TryGetProp(hidden_abil, "Level");
                    var add_factor = TryGetProp(hidden_abil_cls, "FactorByLevel", 0) * 0.01;
                    var add_value = 0;

                    if (abil_level == 10) {
                        add_value = TryGetProp(hidden_abil_cls, "AddFactor", 0) * 0.01
                    }

                    addAbilRate = addAbilRate * (1 + (abil_level * add_factor) + add_value);
                }

            }

        }

    }

    return addAbilRate
}

var value = 155 + skill.Level * 20
value = Math.floor(value * SCR_REINFORCEABILITY_TOOLTIP(skill))
return value;
}
function Effect_CaptionRatio50104(){
function SCR_REINFORCEABILITY_TOOLTIP(skill) {
    var addAbilRate = 1;

    if ("Assassin10" != "None") {
        var reinforceAbil = GetAbility(pc, "Assassin10")

        if (reinforceAbil != null) {
            var abilLevel = TryGetProp(reinforceAbil, "Level")
            var masterAddValue = 0

            if (abilLevel == 100) {
                masterAddValue = 0.1
            }

            addAbilRate = 1 + (reinforceAbil.Level * 0.005 + masterAddValue);
            var hidden_abil_cls = GetClass("HiddenAbility_Reinforce", skill.ClassName);

            if (abilLevel >= 65  &&  hidden_abil_cls != null) {
                var hidden_abil_name = TryGetProp(hidden_abil_cls, "HiddenReinforceAbil");
                var hidden_abil = GetAbility(pc, hidden_abil_name);

                if (hidden_abil != null) {
                    var abil_level = TryGetProp(hidden_abil, "Level");
                    var add_factor = TryGetProp(hidden_abil_cls, "FactorByLevel", 0) * 0.01;
                    var add_value = 0;

                    if (abil_level == 10) {
                        add_value = TryGetProp(hidden_abil_cls, "AddFactor", 0) * 0.01
                    }

                    addAbilRate = addAbilRate * (1 + (abil_level * add_factor) + add_value);
                }

            }

        }

    }

    return addAbilRate
}

var value = 20
value = Math.floor(value * SCR_REINFORCEABILITY_TOOLTIP(skill))
return value;
}
function Effect_CaptionRatio50202(level){
var value = skill.Level
return value
}
function Effect_CaptionRatio50205(level){
var value = 10 * skill.Level
return value;
}
function Effect_CaptionRatio50206(level){
var value = skill.Level * 3

if (IsPVPField(pc) == 1  &&  value > 2) {
    value = Math.floor((Math.pow(Math.max(0, value-2), 0.5)))+Math.min(2, value)
}

return value;
}
function Effect_CaptionRatio50301(level){
return skill.Level;
}
function Effect_CaptionRatio50302(level){
var value = 1 + skill.Level * 1
return value
}
function Effect_CaptionRatio50303(level){
return 1 + skill.Level * 0.5
}
function Effect_CaptionRatio50306(level){
var value = Math.floor(2500 + skill.Level * 250 + ((pc.DEX + pc.STR) * 0.5))
var Squire3 = GetAbility(pc, 'Squire3');
return value
}
function Effect_CaptionRatio50401(level){
function SCR_REINFORCEABILITY_TOOLTIP(skill) {
    var addAbilRate = 1;

    if ("Corsair20" != "None") {
        var reinforceAbil = GetAbility(pc, "Corsair20")

        if (reinforceAbil != null) {
            var abilLevel = TryGetProp(reinforceAbil, "Level")
            var masterAddValue = 0

            if (abilLevel == 100) {
                masterAddValue = 0.1
            }

            addAbilRate = 1 + (reinforceAbil.Level * 0.005 + masterAddValue);
            var hidden_abil_cls = GetClass("HiddenAbility_Reinforce", skill.ClassName);

            if (abilLevel >= 65  &&  hidden_abil_cls != null) {
                var hidden_abil_name = TryGetProp(hidden_abil_cls, "HiddenReinforceAbil");
                var hidden_abil = GetAbility(pc, hidden_abil_name);

                if (hidden_abil != null) {
                    var abil_level = TryGetProp(hidden_abil, "Level");
                    var add_factor = TryGetProp(hidden_abil_cls, "FactorByLevel", 0) * 0.01;
                    var add_value = 0;

                    if (abil_level == 10) {
                        add_value = TryGetProp(hidden_abil_cls, "AddFactor", 0) * 0.01
                    }

                    addAbilRate = addAbilRate * (1 + (abil_level * add_factor) + add_value);
                }

            }

        }

    }

    return addAbilRate
}

var value = 10 + (skill.Level * 1.8)
value = value * SCR_REINFORCEABILITY_TOOLTIP(skill);
return value;
}
function Effect_CaptionRatio50402(level){
var value = 4 + skill.Level * 1;
var zone = GetZoneName(pc);

if (IsPVPServer(pc) == 1  ||  IsPVPField(pc) == 1) {
    value = value * 0.5;
}

return value;
}
function Effect_CaptionRatio50404(){
var value = 500;
return value;
}
function Effect_CaptionRatio50409(level){
var value = 2.5 + (skill.Level * 0.25)
return value
}
function Effect_CaptionRatio50502(){
var value = 10
return value
}
function Effect_CaptionRatio50503(level){
var value = skill.Level * 6
return value
}
function Effect_CaptionRatio50601(level){
return Math.floor(3 + skill.Level * 0.5)
}
function Effect_CaptionRatio50602(level){
return 4 + (skill.Level * 0.4)
}
function Effect_CaptionRatio50604(level){
function SCR_REINFORCEABILITY_TOOLTIP(skill) {
    var addAbilRate = 1;

    if ("Thaumaturge15" != "None") {
        var reinforceAbil = GetAbility(pc, "Thaumaturge15")

        if (reinforceAbil != null) {
            var abilLevel = TryGetProp(reinforceAbil, "Level")
            var masterAddValue = 0

            if (abilLevel == 100) {
                masterAddValue = 0.1
            }

            addAbilRate = 1 + (reinforceAbil.Level * 0.005 + masterAddValue);
            var hidden_abil_cls = GetClass("HiddenAbility_Reinforce", skill.ClassName);

            if (abilLevel >= 65  &&  hidden_abil_cls != null) {
                var hidden_abil_name = TryGetProp(hidden_abil_cls, "HiddenReinforceAbil");
                var hidden_abil = GetAbility(pc, hidden_abil_name);

                if (hidden_abil != null) {
                    var abil_level = TryGetProp(hidden_abil, "Level");
                    var add_factor = TryGetProp(hidden_abil_cls, "FactorByLevel", 0) * 0.01;
                    var add_value = 0;

                    if (abil_level == 10) {
                        add_value = TryGetProp(hidden_abil_cls, "AddFactor", 0) * 0.01
                    }

                    addAbilRate = addAbilRate * (1 + (abil_level * add_factor) + add_value);
                }

            }

        }

    }

    return addAbilRate
}

var value = skill.Level * 100
value = value * SCR_REINFORCEABILITY_TOOLTIP(skill)
return Math.floor(value)
}
function Effect_CaptionRatio50605(level){
var value = 15 + (skill.Level * 10)
return value
}
function Effect_CaptionRatio50606(level){
function SCR_REINFORCEABILITY_TOOLTIP(skill) {
    var addAbilRate = 1;

    if ("Thaumaturge19" != "None") {
        var reinforceAbil = GetAbility(pc, "Thaumaturge19")

        if (reinforceAbil != null) {
            var abilLevel = TryGetProp(reinforceAbil, "Level")
            var masterAddValue = 0

            if (abilLevel == 100) {
                masterAddValue = 0.1
            }

            addAbilRate = 1 + (reinforceAbil.Level * 0.005 + masterAddValue);
            var hidden_abil_cls = GetClass("HiddenAbility_Reinforce", skill.ClassName);

            if (abilLevel >= 65  &&  hidden_abil_cls != null) {
                var hidden_abil_name = TryGetProp(hidden_abil_cls, "HiddenReinforceAbil");
                var hidden_abil = GetAbility(pc, hidden_abil_name);

                if (hidden_abil != null) {
                    var abil_level = TryGetProp(hidden_abil, "Level");
                    var add_factor = TryGetProp(hidden_abil_cls, "FactorByLevel", 0) * 0.01;
                    var add_value = 0;

                    if (abil_level == 10) {
                        add_value = TryGetProp(hidden_abil_cls, "AddFactor", 0) * 0.01
                    }

                    addAbilRate = addAbilRate * (1 + (abil_level * add_factor) + add_value);
                }

            }

        }

    }

    return addAbilRate
}

var maxpatk = SCR_Get_DEFAULT_MAXPATK(pc, value)
var minpatk = SCR_Get_DEFAULT_MINPATK(pc, value)
var value = ((maxpatk + minpatk)/2) * (0.02 + skill.Level * 0.002)
value = (value * SCR_REINFORCEABILITY_TOOLTIP(skill))
return Math.floor(value);
}
function Effect_CaptionRatio50702(level){
return skill.Level + 3
}
function Effect_CaptionRatio50703(level){
var value = 2.5 + skill.Level * 0.5
return Math.floor(value)
}
function Effect_CaptionRatio50705(){
var value = 0;
var casterSTR = TryGetProp(pc, "STR", 0);
var casterCON = TryGetProp(pc, "CON", 0);
var casterINT = TryGetProp(pc, "INT", 0);
var casterMNA = TryGetProp(pc, "MNA", 0);
var casterDEX = TryGetProp(pc, "DEX", 0);
var casterStat = casterSTR + casterCON + casterINT + casterMNA + casterDEX
value = Math.floor(casterStat / 15)
return value;
}
function Effect_CaptionRatio50706(level){
var value = 3 + (skill.Level * 0.5)
return value;
}
function Effect_CaptionRatio50708(level){
var value = 3 + (skill.Level * 0.5)
return value;
}
function Effect_CaptionRatio50801(level){
function SCR_REINFORCEABILITY_TOOLTIP(skill) {
    var addAbilRate = 1;

    if ("Enchanter10" != "None") {
        var reinforceAbil = GetAbility(pc, "Enchanter10")

        if (reinforceAbil != null) {
            var abilLevel = TryGetProp(reinforceAbil, "Level")
            var masterAddValue = 0

            if (abilLevel == 100) {
                masterAddValue = 0.1
            }

            addAbilRate = 1 + (reinforceAbil.Level * 0.005 + masterAddValue);
            var hidden_abil_cls = GetClass("HiddenAbility_Reinforce", skill.ClassName);

            if (abilLevel >= 65  &&  hidden_abil_cls != null) {
                var hidden_abil_name = TryGetProp(hidden_abil_cls, "HiddenReinforceAbil");
                var hidden_abil = GetAbility(pc, hidden_abil_name);

                if (hidden_abil != null) {
                    var abil_level = TryGetProp(hidden_abil, "Level");
                    var add_factor = TryGetProp(hidden_abil_cls, "FactorByLevel", 0) * 0.01;
                    var add_value = 0;

                    if (abil_level == 10) {
                        add_value = TryGetProp(hidden_abil_cls, "AddFactor", 0) * 0.01
                    }

                    addAbilRate = addAbilRate * (1 + (abil_level * add_factor) + add_value);
                }

            }

        }

    }

    return addAbilRate
}

var value = skill.Level * 1.5
value = value * SCR_REINFORCEABILITY_TOOLTIP(skill)
return value;
}
function Effect_CaptionRatio50803(){
function SCR_REINFORCEABILITY_TOOLTIP(skill) {
    var addAbilRate = 1;

    if ("Enchanter11" != "None") {
        var reinforceAbil = GetAbility(pc, "Enchanter11")

        if (reinforceAbil != null) {
            var abilLevel = TryGetProp(reinforceAbil, "Level")
            var masterAddValue = 0

            if (abilLevel == 100) {
                masterAddValue = 0.1
            }

            addAbilRate = 1 + (reinforceAbil.Level * 0.005 + masterAddValue);
            var hidden_abil_cls = GetClass("HiddenAbility_Reinforce", skill.ClassName);

            if (abilLevel >= 65  &&  hidden_abil_cls != null) {
                var hidden_abil_name = TryGetProp(hidden_abil_cls, "HiddenReinforceAbil");
                var hidden_abil = GetAbility(pc, hidden_abil_name);

                if (hidden_abil != null) {
                    var abil_level = TryGetProp(hidden_abil, "Level");
                    var add_factor = TryGetProp(hidden_abil_cls, "FactorByLevel", 0) * 0.01;
                    var add_value = 0;

                    if (abil_level == 10) {
                        add_value = TryGetProp(hidden_abil_cls, "AddFactor", 0) * 0.01
                    }

                    addAbilRate = addAbilRate * (1 + (abil_level * add_factor) + add_value);
                }

            }

        }

    }

    return addAbilRate
}

var sklLv = TryGetProp(skill, "Level", 1)
var value = 5 + sklLv * 1.5
value = value * SCR_REINFORCEABILITY_TOOLTIP(skill)
return Math.floor(value)
}
function Effect_CaptionRatio50804(level){
function SCR_REINFORCEABILITY_TOOLTIP(skill) {
    var addAbilRate = 1;

    if ("Enchanter12" != "None") {
        var reinforceAbil = GetAbility(pc, "Enchanter12")

        if (reinforceAbil != null) {
            var abilLevel = TryGetProp(reinforceAbil, "Level")
            var masterAddValue = 0

            if (abilLevel == 100) {
                masterAddValue = 0.1
            }

            addAbilRate = 1 + (reinforceAbil.Level * 0.005 + masterAddValue);
            var hidden_abil_cls = GetClass("HiddenAbility_Reinforce", skill.ClassName);

            if (abilLevel >= 65  &&  hidden_abil_cls != null) {
                var hidden_abil_name = TryGetProp(hidden_abil_cls, "HiddenReinforceAbil");
                var hidden_abil = GetAbility(pc, hidden_abil_name);

                if (hidden_abil != null) {
                    var abil_level = TryGetProp(hidden_abil, "Level");
                    var add_factor = TryGetProp(hidden_abil_cls, "FactorByLevel", 0) * 0.01;
                    var add_value = 0;

                    if (abil_level == 10) {
                        add_value = TryGetProp(hidden_abil_cls, "AddFactor", 0) * 0.01
                    }

                    addAbilRate = addAbilRate * (1 + (abil_level * add_factor) + add_value);
                }

            }

        }

    }

    return addAbilRate
}

var value = 5 + skill.Level * 1
value = value * SCR_REINFORCEABILITY_TOOLTIP(skill)
return value
}
function Effect_CaptionRatio50806(level){
var maxpatk = SCR_Get_DEFAULT_MAXPATK(pc, 0)
var minpatk = SCR_Get_DEFAULT_MINPATK(pc, 0)
var value = ((maxpatk + minpatk)/2) * (0.015 + skill.Level * 0.004)
return Math.floor(value);
}
function Effect_CaptionRatio50807(level){
function SCR_REINFORCEABILITY_TOOLTIP(skill) {
    var addAbilRate = 1;

    if ("Enchanter9" != "None") {
        var reinforceAbil = GetAbility(pc, "Enchanter9")

        if (reinforceAbil != null) {
            var abilLevel = TryGetProp(reinforceAbil, "Level")
            var masterAddValue = 0

            if (abilLevel == 100) {
                masterAddValue = 0.1
            }

            addAbilRate = 1 + (reinforceAbil.Level * 0.005 + masterAddValue);
            var hidden_abil_cls = GetClass("HiddenAbility_Reinforce", skill.ClassName);

            if (abilLevel >= 65  &&  hidden_abil_cls != null) {
                var hidden_abil_name = TryGetProp(hidden_abil_cls, "HiddenReinforceAbil");
                var hidden_abil = GetAbility(pc, hidden_abil_name);

                if (hidden_abil != null) {
                    var abil_level = TryGetProp(hidden_abil, "Level");
                    var add_factor = TryGetProp(hidden_abil_cls, "FactorByLevel", 0) * 0.01;
                    var add_value = 0;

                    if (abil_level == 10) {
                        add_value = TryGetProp(hidden_abil_cls, "AddFactor", 0) * 0.01
                    }

                    addAbilRate = addAbilRate * (1 + (abil_level * add_factor) + add_value);
                }

            }

        }

    }

    return addAbilRate
}

var value = 5 + (skill.Level)
value = value * SCR_REINFORCEABILITY_TOOLTIP(skill)
return value;
}
function Effect_CaptionRatio50901(level){
return 10 + skill.Level * 2;
}
function Effect_CaptionRatio50902(level){
return 15 + skill.Level * 1.5;
}
function Effect_CaptionRatio50903(level){
var value = 50 * skill.Level
return value
}
function Effect_CaptionRatio50907(level){
var value = 5 + (skill.Level * 1)

if (IsPVPServer(pc) == 1  ||  IsPVPField(pc) == 1) {
    value = value * 0.5;
}

return value;
}
function Effect_CaptionRatio51002(level){
var value = skill.Level * 0.5
var abil = GetAbility(pc, "Schwarzereiter16")

if (abil != null  &&  TryGetProp(abil, "ActiveState", 0) == 1) {
    value = value * 2
}

return value;
}
function Effect_CaptionRatio51003(){
var value = 12;
var lv = pc.Lv
var bylvCorrect = lv - 300

if (bylvCorrect < 0) {
    bylvCorrect = bylvCorrect * 2.75 / 1000
} else if (bylvCorrect >= 0) {
    bylvCorrect = bylvCorrect * 1.25 / 1000
}

value = value * (1 + bylvCorrect)
var abilSchwarzereiter18 = GetAbility(pc, 'Schwarzereiter18');

if (abilSchwarzereiter18 != null) {
    value = value + 5;
}

return Math.floor(value)
}
function Effect_CaptionRatio51005(level){
function SCR_REINFORCEABILITY_TOOLTIP(skill) {
    var addAbilRate = 1;

    if ("Schwarzereiter33" != "None") {
        var reinforceAbil = GetAbility(pc, "Schwarzereiter33")

        if (reinforceAbil != null) {
            var abilLevel = TryGetProp(reinforceAbil, "Level")
            var masterAddValue = 0

            if (abilLevel == 100) {
                masterAddValue = 0.1
            }

            addAbilRate = 1 + (reinforceAbil.Level * 0.005 + masterAddValue);
            var hidden_abil_cls = GetClass("HiddenAbility_Reinforce", skill.ClassName);

            if (abilLevel >= 65  &&  hidden_abil_cls != null) {
                var hidden_abil_name = TryGetProp(hidden_abil_cls, "HiddenReinforceAbil");
                var hidden_abil = GetAbility(pc, hidden_abil_name);

                if (hidden_abil != null) {
                    var abil_level = TryGetProp(hidden_abil, "Level");
                    var add_factor = TryGetProp(hidden_abil_cls, "FactorByLevel", 0) * 0.01;
                    var add_value = 0;

                    if (abil_level == 10) {
                        add_value = TryGetProp(hidden_abil_cls, "AddFactor", 0) * 0.01
                    }

                    addAbilRate = addAbilRate * (1 + (abil_level * add_factor) + add_value);
                }

            }

        }

    }

    return addAbilRate
}

var value = skill.Level * 6
var abil = GetAbility(pc, "Schwarzereiter33")

if (abil != null  &&  TryGetProp(abil, "ActiveState", 0) == 1) {
    value = value * SCR_REINFORCEABILITY_TOOLTIP(skill);
}

return value
}
function Effect_CaptionRatio51006(){
var value = 15

if (IsPVPField(pc) == 1  &&  value > 2) {
    value = Math.floor((Math.pow(Math.max(0, value-2), 0.5)))+Math.min(2, value)
}

return value
}
function Effect_CaptionRatio51102(){
var value = 10
var abil = GetAbility(pc, "Bulletmarker7")

if (abil != null  &&  abil.ActiveState == 1) {
    value = value + abil.Level
}

return value
}
function Effect_CaptionRatio51109(level){
var value = 10 + skill.Level * 2
return value;
}
function Effect_CaptionRatio51111(){
var value = 30

if (IsPVPServer(pc) == 1) {
    value = value / 2
}

return value
}
function Effect_CaptionRatio51112(){
var arg1 = TryGetProp(skill, 'Level', '1')
var value = 100 + arg1 * 10
return value
}
function Effect_CaptionRatio51204(level){
function SCR_REINFORCEABILITY_TOOLTIP(skill) {
    var addAbilRate = 1;

    if ("Arditi5" != "None") {
        var reinforceAbil = GetAbility(pc, "Arditi5")

        if (reinforceAbil != null) {
            var abilLevel = TryGetProp(reinforceAbil, "Level")
            var masterAddValue = 0

            if (abilLevel == 100) {
                masterAddValue = 0.1
            }

            addAbilRate = 1 + (reinforceAbil.Level * 0.005 + masterAddValue);
            var hidden_abil_cls = GetClass("HiddenAbility_Reinforce", skill.ClassName);

            if (abilLevel >= 65  &&  hidden_abil_cls != null) {
                var hidden_abil_name = TryGetProp(hidden_abil_cls, "HiddenReinforceAbil");
                var hidden_abil = GetAbility(pc, hidden_abil_name);

                if (hidden_abil != null) {
                    var abil_level = TryGetProp(hidden_abil, "Level");
                    var add_factor = TryGetProp(hidden_abil_cls, "FactorByLevel", 0) * 0.01;
                    var add_value = 0;

                    if (abil_level == 10) {
                        add_value = TryGetProp(hidden_abil_cls, "AddFactor", 0) * 0.01
                    }

                    addAbilRate = addAbilRate * (1 + (abil_level * add_factor) + add_value);
                }

            }

        }

    }

    return addAbilRate
}

var value = skill.Level + 5
value = value * SCR_REINFORCEABILITY_TOOLTIP(skill)
return Math.floor(value)
}
function Effect_CaptionRatio51206(){
var value = 10
return value
}
function Effect_CaptionRatio51302(){
var value = Math.min(4 + Math.floor(TryGetProp(pc, 'SR', 0) / 2), 10);

if (IsPVPField(pc) == 1  &&  value > 2) {
    value = Math.floor((Math.pow(Math.max(0, value-2), 0.5)))+Math.min(2, value)
}

return value
}
function Effect_CaptionRatio51303(level){
var value = Math.floor(4 + skill.Level * 1)
return value
}
function Effect_CaptionRatio51304(level){
var value = 3 + (skill.Level - 1) * 0.5
return value
}
function Effect_CaptionRatio51305(level){
var value = Math.ceil(skill.Level * 0.5)
var abil = GetAbility(pc, 'Sheriff6')

if (abil != null  &&  abil.ActiveState == 1) {
    value = value * 2;
}

return value
}
function Effect_CaptionRatio51306(){
var value = 3
var abil = GetAbility(pc, "Sheriff5")

if (abil != null  &&  abil.ActiveState == 1) {
    value = 1
}

return value
}
function Effect_CaptionRatio51404(){
function SCR_REINFORCEABILITY_TOOLTIP(skill) {
    var addAbilRate = 1;

    if ("Rangda13" != "None") {
        var reinforceAbil = GetAbility(pc, "Rangda13")

        if (reinforceAbil != null) {
            var abilLevel = TryGetProp(reinforceAbil, "Level")
            var masterAddValue = 0

            if (abilLevel == 100) {
                masterAddValue = 0.1
            }

            addAbilRate = 1 + (reinforceAbil.Level * 0.005 + masterAddValue);
            var hidden_abil_cls = GetClass("HiddenAbility_Reinforce", skill.ClassName);

            if (abilLevel >= 65  &&  hidden_abil_cls != null) {
                var hidden_abil_name = TryGetProp(hidden_abil_cls, "HiddenReinforceAbil");
                var hidden_abil = GetAbility(pc, hidden_abil_name);

                if (hidden_abil != null) {
                    var abil_level = TryGetProp(hidden_abil, "Level");
                    var add_factor = TryGetProp(hidden_abil_cls, "FactorByLevel", 0) * 0.01;
                    var add_value = 0;

                    if (abil_level == 10) {
                        add_value = TryGetProp(hidden_abil_cls, "AddFactor", 0) * 0.01
                    }

                    addAbilRate = addAbilRate * (1 + (abil_level * add_factor) + add_value);
                }

            }

        }

    }

    return addAbilRate
}

var sklLv = TryGetProp(skill, "Level", 1)
var value = 10 + sklLv * 5
value = value * SCR_REINFORCEABILITY_TOOLTIP(skill)
return Math.floor(value)
}
function Effect_CaptionRatio51405(level){
var value = 0.5 * skill.Level;
return value
}
function Effect_CaptionRatio51406(){
var value = 2;
return value
}
function Effect_CaptionRatio51501(){
var value = 1000
var GuidedShotSkill = GetSkill(pc, 'Clown_Replica');

if (GuidedShotSkill != null) {
    value = TryGetProp(GuidedShotSkill, "SkillFactor", 1000) * 0.3
}

return value
}
function Effect_CaptionRatio51503(){
var value = 7

if (IsPVPField(pc) == 1  &&  value > 2) {
    value = Math.floor((Math.pow(Math.max(0, value-2), 0.5)))+Math.min(2, value)
}

return value
}
function Effect_CaptionRatio51504(){
var value = 1000
var GuidedShotSkill = GetSkill(pc, 'Clown_Replica');

if (GuidedShotSkill != null) {
    value = TryGetProp(GuidedShotSkill, "SkillFactor", 1000) * 0.3
}

return value
}
function Effect_CaptionRatio51505(level){
function SCR_REINFORCEABILITY_TOOLTIP(skill) {
    var addAbilRate = 1;

    if ("Clown5" != "None") {
        var reinforceAbil = GetAbility(pc, "Clown5")

        if (reinforceAbil != null) {
            var abilLevel = TryGetProp(reinforceAbil, "Level")
            var masterAddValue = 0

            if (abilLevel == 100) {
                masterAddValue = 0.1
            }

            addAbilRate = 1 + (reinforceAbil.Level * 0.005 + masterAddValue);
            var hidden_abil_cls = GetClass("HiddenAbility_Reinforce", skill.ClassName);

            if (abilLevel >= 65  &&  hidden_abil_cls != null) {
                var hidden_abil_name = TryGetProp(hidden_abil_cls, "HiddenReinforceAbil");
                var hidden_abil = GetAbility(pc, hidden_abil_name);

                if (hidden_abil != null) {
                    var abil_level = TryGetProp(hidden_abil, "Level");
                    var add_factor = TryGetProp(hidden_abil_cls, "FactorByLevel", 0) * 0.01;
                    var add_value = 0;

                    if (abil_level == 10) {
                        add_value = TryGetProp(hidden_abil_cls, "AddFactor", 0) * 0.01
                    }

                    addAbilRate = addAbilRate * (1 + (abil_level * add_factor) + add_value);
                }

            }

        }

    }

    return addAbilRate
}

var value = skill.Level * 0.5
value = value * SCR_REINFORCEABILITY_TOOLTIP(skill);
return value;
}
function Effect_CaptionRatio51506(){
var value = TryGetProp(skill, "Level", 1)

if (IsPVPField(pc) == 1  &&  value > 2) {
    value = Math.floor((Math.pow(Math.max(0, value-2), 0.5)))+Math.min(2, value)
}

return value
}
