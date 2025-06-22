from unittest import TestCase

from ..utils import cantonese_utils


class TestExtractJyutpingTones(TestCase):
    def test_simple(self):
        string = "zeng3 je5"
        res = cantonese_utils.extract_jyutping_tones(string)
        self.assertEqual(res, [3, 5])

    def test_no_spaces(self):
        string = "zeng3je5"
        res = cantonese_utils.extract_jyutping_tones(string)
        self.assertEqual(res, [3, 5])

    def test_bad_numeric(self):
        string = "㒃"
        res = cantonese_utils.extract_jyutping_tones(string)
        self.assertEqual(res, [])


class TestJyutpingToYale(TestCase):
    def test_simple(self):
        res = cantonese_utils.jyutping_to_yale("si1 zi2 saan1")
        self.assertEqual(res, "sī jí sāan")

    def test_reject_no_tone(self):
        res = cantonese_utils.jyutping_to_yale("joeng")
        self.assertEqual(res, "joeng")

    def test_reject_single_letter(self):
        res = cantonese_utils.jyutping_to_yale("a")
        self.assertEqual(res, "a")

    def test_reject_special_character(self):
        res = cantonese_utils.jyutping_to_yale("-")
        self.assertEqual(res, "-")

    def test_no_spaces(self):
        res = cantonese_utils.jyutping_to_yale("si1zi2saan1")
        self.assertEqual(res, "sī jí sāan")

    def test_spaces_to_segment(self):
        res = cantonese_utils.jyutping_to_yale(
            "si1 zi2 saan1", use_spaces_to_segment=True
        )
        self.assertEqual(res, "sī jí sāan")

    def test_special_final(self):
        res = cantonese_utils.jyutping_to_yale("goek3jyun5")
        self.assertEqual(res, "geuk yúhn")

    def test_light_tone(self):
        res = cantonese_utils.jyutping_to_yale("lok6 jyu5")
        self.assertEqual(res, "lohk yúh")

    def test_special_syllable(self):
        res = cantonese_utils.jyutping_to_yale("m4 hai6")
        self.assertEqual(res, "m̀h haih")

    def test_tones(self):
        res = cantonese_utils.jyutping_to_yale(
            "saam1 gau2 sei3 ling4 ng5 ji6 cat1 baat3 luk6"
        )
        self.assertEqual(res, "sāam gáu sei lìhng ńgh yih chāt baat luhk")

    def test_no_tone(self):
        res = cantonese_utils.jyutping_to_yale("mit")
        self.assertEqual(res, "mit")

    def test_malformed_space(self):
        res = cantonese_utils.jyutping_to_yale("mat 6")
        self.assertEqual(res, "mat 6")


class TestJyutpingToIPA(TestCase):
    def test_simple(self):
        res = cantonese_utils.jyutping_to_IPA("joeng4 sing4")
        self.assertEqual(res, "jœ̽ːŋ˨˩ sɪŋ˨˩")

    def test_reject_no_tone(self):
        res = cantonese_utils.jyutping_to_IPA("joeng")
        self.assertEqual(res, "joeng")

    def test_reject_single_letter(self):
        res = cantonese_utils.jyutping_to_IPA("a")
        self.assertEqual(res, "a")

    def test_reject_special_character(self):
        res = cantonese_utils.jyutping_to_IPA("-")
        self.assertEqual(res, "-")

    def test_no_spaces(self):
        res = cantonese_utils.jyutping_to_IPA("faa1sing4")
        self.assertEqual(res, "fäː˥ sɪŋ˨˩")

    def test_spaces_to_segment(self):
        res = cantonese_utils.jyutping_to_IPA("joeng4 sing4", use_spaces_to_segment=True)
        self.assertEqual(res, "jœ̽ːŋ˨˩ sɪŋ˨˩")

    def test_preprocess_initial(self):
        res = cantonese_utils.jyutping_to_IPA("zyu2 sung3")
        self.assertEqual(res, "t͡ʃyː˧˥ sʊŋ˧")

    def test_special_syllable(self):
        res = cantonese_utils.jyutping_to_IPA("m4")
        self.assertEqual(res, "m̩˨˩")

    def test_checked_tone(self):
        res = cantonese_utils.jyutping_to_IPA("sik6 si2 o1 faan6")
        self.assertEqual(res, "sɪk̚˨ siː˧˥ ɔː˥ fäːn˨")

    def test_special_final(self):
        res = cantonese_utils.jyutping_to_IPA("uk1 kei2 jan4")
        self.assertEqual(res, "ʊk̚˥ kʰei̯˧˥ jɐn˨˩")

    def test_tones(self):
        res = cantonese_utils.jyutping_to_IPA(
            "saam1 gau2 sei3 ling4 ng5 ji6 cat1 baat3 luk6"
        )
        self.assertEqual(res, "säːm˥ kɐu̯˧˥ sei̯˧ lɪŋ˨˩ ŋ̍˩˧ jiː˨ t͡sʰɐt̚˥ päːt̚˧ lʊk̚˨")

    def test_no_tone(self):
        res = cantonese_utils.jyutping_to_yale("mok")
        self.assertEqual(res, "mok")


class TestJyutpingAutocorrect(TestCase):
    def test_hui(self):
        res = cantonese_utils.jyutping_autocorrect("hui")
        self.assertEqual(res, "heoi")

        res = cantonese_utils.jyutping_autocorrect("shui")
        self.assertEqual(res, "seoi")

    def test_cu(self):
        res = cantonese_utils.jyutping_autocorrect("cui")
        self.assertEqual(res, "(k)(eo|u)i")

        res = cantonese_utils.jyutping_autocorrect("cum")
        self.assertEqual(res, "(k)am")

    def test_x(self):
        res = cantonese_utils.jyutping_autocorrect("xuet")
        self.assertEqual(res, "s(yu)t")

        res = cantonese_utils.jyutping_autocorrect("xui")
        self.assertEqual(res, "s(eo|u)i")

    def test_ch(self):
        res = cantonese_utils.jyutping_autocorrect("choeng")
        self.assertEqual(res, "coeng")

        res = cantonese_utils.jyutping_autocorrect("chi")
        self.assertEqual(res, "ci")

    def test_sh(self):
        res = cantonese_utils.jyutping_autocorrect("shoeng")
        self.assertEqual(res, "soeng")

        res = cantonese_utils.jyutping_autocorrect("shi")
        self.assertEqual(res, "si")

    def test_zh(self):
        res = cantonese_utils.jyutping_autocorrect("zhoeng")
        self.assertEqual(res, "zoeng")

        res = cantonese_utils.jyutping_autocorrect("zhi")
        self.assertEqual(res, "zi")

    def test_eung_erng_eong(self):
        res = cantonese_utils.jyutping_autocorrect("zeung")
        self.assertEqual(res, "zoeng")

        res = cantonese_utils.jyutping_autocorrect("zerng")
        self.assertEqual(res, "zoeng")

        res = cantonese_utils.jyutping_autocorrect("zeong")
        self.assertEqual(res, "zoeng")

    def test_eui(self):
        res = cantonese_utils.jyutping_autocorrect("zeui")
        self.assertEqual(res, "zeoi")

    def test_euk(self):
        res = cantonese_utils.jyutping_autocorrect("seuk")
        self.assertEqual(res, "soek")

    def test_eun(self):
        res = cantonese_utils.jyutping_autocorrect("ceun")
        self.assertEqual(res, "c(eo|yu)n")

    def test_eut(self):
        res = cantonese_utils.jyutping_autocorrect("seut")
        self.assertEqual(res, "s(eo|yu)t")

    def test_eu(self):
        res = cantonese_utils.jyutping_autocorrect("zeu")
        self.assertEqual(res, "z(e|y)u")

    def test_ern(self):
        res = cantonese_utils.jyutping_autocorrect("zern")
        self.assertEqual(res, "zeon")

    def test_oen(self):
        res = cantonese_utils.jyutping_autocorrect("zoen")
        self.assertEqual(res, "zeon")

    def test_ao(self):
        res = cantonese_utils.jyutping_autocorrect("haagao")
        self.assertEqual(res, "haagau")

        res = cantonese_utils.jyutping_autocorrect("gaolyun")
        self.assertEqual(res, "gaol(ja|jyu|yu)n")

    def test_ar(self):
        res = cantonese_utils.jyutping_autocorrect("char")
        self.assertEqual(res, "caa")

    def test_ee(self):
        res = cantonese_utils.jyutping_autocorrect("see")
        self.assertEqual(res, "si")

    def test_ay(self):
        res = cantonese_utils.jyutping_autocorrect("hay")
        self.assertEqual(res, "hei")

    def test_oy(self):
        res = cantonese_utils.jyutping_autocorrect("choy")
        self.assertEqual(res, "coi")

    def test_oo(self):
        res = cantonese_utils.jyutping_autocorrect("soot")
        self.assertEqual(res, "s(y!u)t")

    def test_ong(self):
        res = cantonese_utils.jyutping_autocorrect("fong")
        self.assertEqual(res, "f(o|u)ng")

    def test_young(self):
        res = cantonese_utils.jyutping_autocorrect("young")
        self.assertEqual(res, "j(y!u|a|eo)ng")

    def test_yue(self):
        res = cantonese_utils.jyutping_autocorrect("yuet")
        self.assertEqual(res, "j(yu)t")

    def test_ue(self):
        res = cantonese_utils.jyutping_autocorrect("tsuen")
        self.assertEqual(res, "c(yu)n")

    def test_tsz(self):
        res = cantonese_utils.jyutping_autocorrect("tsz")
        self.assertEqual(res, "zi")

    def test_ck(self):
        res = cantonese_utils.jyutping_autocorrect("back")
        self.assertEqual(res, "bak")

    def test_ey(self):
        res = cantonese_utils.jyutping_autocorrect("gey ")
        self.assertEqual(res, "gei ")

        res = cantonese_utils.jyutping_autocorrect("gey'")
        self.assertEqual(res, "gei'")

        res = cantonese_utils.jyutping_autocorrect("gey")
        self.assertEqual(res, "gei")

        res = cantonese_utils.jyutping_autocorrect("geyhey")
        self.assertEqual(res, "geihei")

        res = cantonese_utils.jyutping_autocorrect("peylou")
        self.assertEqual(res, "peilou")

        res = cantonese_utils.jyutping_autocorrect("yeye")
        self.assertEqual(res, "je je")

        res = cantonese_utils.jyutping_autocorrect("beycaam")
        self.assertEqual(res, "beicaam")

        res = cantonese_utils.jyutping_autocorrect("geye")
        self.assertEqual(res, "ge je")

        res = cantonese_utils.jyutping_autocorrect("geyegeye beycaamyeyeyeyeyeyeyepeylougeyheygeygey'gey")
        self.assertEqual(res, "ge jege je beicaamje je je je je je jepeilougeiheigeigei'gei")

    def test_oh(self):
        res = cantonese_utils.jyutping_autocorrect("moh ")
        self.assertEqual(res, "mou ")

        res = cantonese_utils.jyutping_autocorrect("moh'")
        self.assertEqual(res, "mou'")

        res = cantonese_utils.jyutping_autocorrect("moh")
        self.assertEqual(res, "mou")

        res = cantonese_utils.jyutping_autocorrect("ohoh")
        self.assertEqual(res, "ouou")

        res = cantonese_utils.jyutping_autocorrect("nohdoi")
        self.assertEqual(res, "noudoi")

        res = cantonese_utils.jyutping_autocorrect("lohjan")
        self.assertEqual(res, "loujan")

        res = cantonese_utils.jyutping_autocorrect("lohon")
        self.assertEqual(res, "lo hon")

        res = cantonese_utils.jyutping_autocorrect("mohmohmohlohonlohonlohjannohdoimoh moh")
        self.assertEqual(res, "moumoumoulo honlo honloujannoudoimou mou")

    def test_ow(self):
        res = cantonese_utils.jyutping_autocorrect("gow ")
        self.assertEqual(res, "gau ")

        res = cantonese_utils.jyutping_autocorrect("gow'")
        self.assertEqual(res, "gau'")

        res = cantonese_utils.jyutping_autocorrect("gow ")
        self.assertEqual(res, "gau ")

        res = cantonese_utils.jyutping_autocorrect("mow")
        self.assertEqual(res, "mau")

        res = cantonese_utils.jyutping_autocorrect("towgai")
        self.assertEqual(res, "taugai")

        res = cantonese_utils.jyutping_autocorrect("gowcat")
        self.assertEqual(res, "gaucat")

        res = cantonese_utils.jyutping_autocorrect("howu")
        self.assertEqual(res, "ho wu")

        res = cantonese_utils.jyutping_autocorrect("mowmowmowhowuho wu towgai")
        self.assertEqual(res, "maumaumauho wuho wu taugai")

    def test_um(self):
        res = cantonese_utils.jyutping_autocorrect("gum ")
        self.assertEqual(res, "gam ")

        res = cantonese_utils.jyutping_autocorrect("gum'")
        self.assertEqual(res, "gam'")

        res = cantonese_utils.jyutping_autocorrect("gum")
        self.assertEqual(res, "gam")

        res = cantonese_utils.jyutping_autocorrect("bum")
        self.assertEqual(res, "bam")

        res = cantonese_utils.jyutping_autocorrect("bumbumbumbum")
        self.assertEqual(res, "bambambambam")

        res = cantonese_utils.jyutping_autocorrect("wumit")
        self.assertEqual(res, "wumit")

        res = cantonese_utils.jyutping_autocorrect("gumzau")
        self.assertEqual(res, "gamzau")

        res = cantonese_utils.jyutping_autocorrect("guman")
        self.assertEqual(res, "gu man")

        res = cantonese_utils.jyutping_autocorrect("gumangumzauwumitbumbumbumbum")
        self.assertEqual(res, "gu mangamzauwumitbambambambam")

    def test_yum(self):
        res = cantonese_utils.jyutping_autocorrect("yum ")
        self.assertEqual(res, "jam ")

        res = cantonese_utils.jyutping_autocorrect("yum'")
        self.assertEqual(res, "jam'")

        res = cantonese_utils.jyutping_autocorrect("yum")
        self.assertEqual(res, "jam")

        res = cantonese_utils.jyutping_autocorrect("cyumat")
        self.assertEqual(res, "cyu mat")

        res = cantonese_utils.jyutping_autocorrect("syuyum")
        self.assertEqual(res, "syujam")

        res = cantonese_utils.jyutping_autocorrect("cyumatcyumatcyumatsyuyumyumyum")
        self.assertEqual(res, "cyu matcyu matcyu matsyujamjamjam")

    def test_yup(self):
        res = cantonese_utils.jyutping_autocorrect("yup ")
        self.assertEqual(res, "jap ")

        res = cantonese_utils.jyutping_autocorrect("yup'")
        self.assertEqual(res, "jap'")

        res = cantonese_utils.jyutping_autocorrect("yup")
        self.assertEqual(res, "jap")

        res = cantonese_utils.jyutping_autocorrect("syupei")
        self.assertEqual(res, "syu pei")

        res = cantonese_utils.jyutping_autocorrect("zeonyup")
        self.assertEqual(res, "zeonjap")

        res = cantonese_utils.jyutping_autocorrect("zeonyupzeonyupsyupeisyupeiyupyupzeonyup")
        self.assertEqual(res, "zeonjapzeonjapsyu peisyu peijapjapzeonjap")

    def test_yuk(self):
        res = cantonese_utils.jyutping_autocorrect("yuk")
        self.assertEqual(res, "juk")

        res = cantonese_utils.jyutping_autocorrect(" yuk")
        self.assertEqual(res, " juk")

        res = cantonese_utils.jyutping_autocorrect("geyyuk")
        self.assertEqual(res, "geijuk")

        res = cantonese_utils.jyutping_autocorrect("gey yuk")
        self.assertEqual(res, "gei juk")

        res = cantonese_utils.jyutping_autocorrect("jyukap")
        self.assertEqual(res, "jyu kap")

        res = cantonese_utils.jyutping_autocorrect("jyu kap")
        self.assertEqual(res, "jyu kap")

        res = cantonese_utils.jyutping_autocorrect("jyu kapgey yukgeyyukyukyukyukyuk yuk")
        self.assertEqual(res, "jyu kapgei jukgeijukjukjukjukjuk juk")

    def test_jung(self):
        res = cantonese_utils.jyutping_autocorrect("yung")
        self.assertEqual(res, "j(y!u|a|eo)ng")

        res = cantonese_utils.jyutping_autocorrect(" yung")
        self.assertEqual(res, " j(y!u|a|eo)ng")

        res = cantonese_utils.jyutping_autocorrect("gumyung")
        self.assertEqual(res, "gamj(y!u|a|eo)ng")

        res = cantonese_utils.jyutping_autocorrect("zyungaa")
        self.assertEqual(res, "z(yu)n gaa")

        res = cantonese_utils.jyutping_autocorrect("jyungin")
        self.assertEqual(res, "j(yu)n gin")

        res = cantonese_utils.jyutping_autocorrect("jyungingumyung yungyungyungzyungaa")
        self.assertEqual(res, "j(yu)n gingamj(y!u|a|eo)ng j(y!u|a|eo)ngj(y!u|a|eo)ngj(y!u|a|eo)ngz(yu)n gaa")

    def test_yun(self):
        res = cantonese_utils.jyutping_autocorrect("yun")
        self.assertEqual(res, "j(a|yu)n")

        res = cantonese_utils.jyutping_autocorrect(" yun")
        self.assertEqual(res, " (ja|jyu|yu)n")

        res = cantonese_utils.jyutping_autocorrect("gumyun")
        self.assertEqual(res, "gam(ja|jyu|yu)n")

        res = cantonese_utils.jyutping_autocorrect("syuntau")
        self.assertEqual(res, "sy(y!u|a|eo)ntau")

        res = cantonese_utils.jyutping_autocorrect("syuntausyuntaugumyunyun yunyunyun")
        self.assertEqual(
            res, "sy(y!u|a|eo)ntausy(y!u|a|eo)ntaugam(ja|jyu|yu)n(ja|jyu|yu)n (ja|jyu|yu)n(ja|jyu|yu)n(ja|jyu|yu)n")

    def test_yut(self):
        res = cantonese_utils.jyutping_autocorrect("yut")
        self.assertEqual(res, "j(a|yu)t")

        res = cantonese_utils.jyutping_autocorrect(" yut")
        self.assertEqual(res, " (ja|jyu|yu)t")

        res = cantonese_utils.jyutping_autocorrect("gamyut")
        self.assertEqual(res, "gam(ja|jyu|yu)t")

        res = cantonese_utils.jyutping_autocorrect("jyutjyu")
        self.assertEqual(res, "j(yu)tjyu")

        res = cantonese_utils.jyutping_autocorrect("zyutai")
        self.assertEqual(res, "z(yu)tai")

        res = cantonese_utils.jyutping_autocorrect("zyutaijyutjyugamyut yut yutyutyut")
        self.assertEqual(res, "z(yu)taij(yu)tjyugam(ja|jyu|yu)t (ja|jyu|yu)t (ja|jyu|yu)t(ja|jyu|yu)t(ja|jyu|yu)t")

    def test_y(self):
        res = cantonese_utils.jyutping_autocorrect("yaang")
        self.assertEqual(res, "jaang")

        res = cantonese_utils.jyutping_autocorrect("yeng")
        self.assertEqual(res, "jeng")

        res = cantonese_utils.jyutping_autocorrect("yuen")
        self.assertEqual(res, "jy(y!u|a|eo)n")

    def test_ui(self):
        res = cantonese_utils.jyutping_autocorrect("gui")
        self.assertEqual(res, "g(eo|u)i")

        res = cantonese_utils.jyutping_autocorrect(" gui")
        self.assertEqual(res, " g(eo|u)i")

        res = cantonese_utils.jyutping_autocorrect("yumsui")
        self.assertEqual(res, "jams(eo|u)i")

    def test_un(self):
        res = cantonese_utils.jyutping_autocorrect("gun")
        self.assertEqual(res, "g(y!u|a|eo)n")

        res = cantonese_utils.jyutping_autocorrect(" gun")
        self.assertEqual(res, " g(y!u|a|eo)n")

        res = cantonese_utils.jyutping_autocorrect("gunzoeng")
        self.assertEqual(res, "g(y!u|a|eo)nzoeng")

    def test_ut(self):
        res = cantonese_utils.jyutping_autocorrect("gut")
        self.assertEqual(res, "g(a|y!u)t")

        res = cantonese_utils.jyutping_autocorrect(" gut")
        self.assertEqual(res, " g(a|y!u)t")

        res = cantonese_utils.jyutping_autocorrect("gumgut")
        self.assertEqual(res, "gamg(a|y!u)t")

        res = cantonese_utils.jyutping_autocorrect("shut goh")
        self.assertEqual(res, "s(a|y!u)t gou")


class TestJyutpingSoundChanges(TestCase):
    def test_ng(self):
        res = cantonese_utils.jyutping_sound_changes(["ng"])
        self.assertEqual(res, ["(ng|m)"])

        res = cantonese_utils.jyutping_sound_changes(["ng4"])
        self.assertEqual(res, ["(ng|m)4"])

        res = cantonese_utils.jyutping_sound_changes(["ng?"])
        self.assertEqual(res, ["(ng|m)?"])

    def test_m(self):
        res = cantonese_utils.jyutping_sound_changes(["m"])
        self.assertEqual(res, ["(ng|m)"])

        res = cantonese_utils.jyutping_sound_changes(["m4"])
        self.assertEqual(res, ["(ng|m)4"])

        res = cantonese_utils.jyutping_sound_changes(["m?"])
        self.assertEqual(res, ["(ng|m)?"])

    def test_ng_initial(self):
        res = cantonese_utils.jyutping_sound_changes(["ngo"])
        self.assertEqual(res, ["(ng)!o"])

        res = cantonese_utils.jyutping_sound_changes(["ngo5"])
        self.assertEqual(res, ["(ng)!o5"])

        res = cantonese_utils.jyutping_sound_changes(["ngo?"])
        self.assertEqual(res, ["(ng)!o?"])

    def test_null_initial(self):
        res = cantonese_utils.jyutping_sound_changes(["o"])
        self.assertEqual(res, ["(ng)!o"])

        res = cantonese_utils.jyutping_sound_changes(["o5"])
        self.assertEqual(res, ["(ng)!o5"])

        res = cantonese_utils.jyutping_sound_changes(["o?"])
        self.assertEqual(res, ["(ng)!o?"])

        res = cantonese_utils.jyutping_sound_changes(["ang"])
        self.assertEqual(res, ["(ng)!aa!ng!"])

        res = cantonese_utils.jyutping_sound_changes(["ang2"])
        self.assertEqual(res, ["(ng)!aa!ng!2"])

        res = cantonese_utils.jyutping_sound_changes(["ang?"])
        self.assertEqual(res, ["(ng)!aa!ng!?"])

        res = cantonese_utils.jyutping_sound_changes(["uk"])
        self.assertEqual(res, ["(ng)!uk"])

        res = cantonese_utils.jyutping_sound_changes(["uk1"])
        self.assertEqual(res, ["(ng)!uk1"])

        res = cantonese_utils.jyutping_sound_changes(["uk?"])
        self.assertEqual(res, ["(ng)!uk?"])

    def test_n_initial(self):
        res = cantonese_utils.jyutping_sound_changes(["nei"])
        self.assertEqual(res, ["(n|l)ei"])

        res = cantonese_utils.jyutping_sound_changes(["nei5"])
        self.assertEqual(res, ["(n|l)ei5"])

        res = cantonese_utils.jyutping_sound_changes(["nei?"])
        self.assertEqual(res, ["(n|l)ei?"])

    def test_l_initial(self):
        res = cantonese_utils.jyutping_sound_changes(["lei"])
        self.assertEqual(res, ["(n|l)ei"])

        res = cantonese_utils.jyutping_sound_changes(["lei5"])
        self.assertEqual(res, ["(n|l)ei5"])

        res = cantonese_utils.jyutping_sound_changes(["lei?"])
        self.assertEqual(res, ["(n|l)ei?"])

    def test_gw(self):
        res = cantonese_utils.jyutping_sound_changes(["gok"])
        self.assertEqual(res, ["(g|k)w!o(k|t)"])

        res = cantonese_utils.jyutping_sound_changes(["gok3"])
        self.assertEqual(res, ["(g|k)w!o(k|t)3"])

        res = cantonese_utils.jyutping_sound_changes(["gok?"])
        self.assertEqual(res, ["(g|k)w!o(k|t)?"])

        res = cantonese_utils.jyutping_sound_changes(["g(o|u)ng"])
        self.assertEqual(res, ["(g|k)w!(o|u)ng"])

        res = cantonese_utils.jyutping_sound_changes(["g(o|u)ng3"])
        self.assertEqual(res, ["(g|k)w!(o|u)ng3"])

        res = cantonese_utils.jyutping_sound_changes(["g(o|u)ng?"])
        self.assertEqual(res, ["(g|k)w!(o|u)ng?"])

    def test_kw(self):
        res = cantonese_utils.jyutping_sound_changes(["kok"])
        self.assertEqual(res, ["(g|k)w!o(k|t)"])

        res = cantonese_utils.jyutping_sound_changes(["kok3"])
        self.assertEqual(res, ["(g|k)w!o(k|t)3"])

        res = cantonese_utils.jyutping_sound_changes(["kok?"])
        self.assertEqual(res, ["(g|k)w!o(k|t)?"])

        res = cantonese_utils.jyutping_sound_changes(["k(o|u)ng"])
        self.assertEqual(res, ["(g|k)w!(o|u)ng"])

        res = cantonese_utils.jyutping_sound_changes(["k(o|u)ng3"])
        self.assertEqual(res, ["(g|k)w!(o|u)ng3"])

        res = cantonese_utils.jyutping_sound_changes(["k(o|u)ng?"])
        self.assertEqual(res, ["(g|k)w!(o|u)ng?"])

    def test_d(self):
        res = cantonese_utils.jyutping_sound_changes(["deng"])
        self.assertEqual(res, ["(d|t)eng"])

        res = cantonese_utils.jyutping_sound_changes(["deng1"])
        self.assertEqual(res, ["(d|t)eng1"])

        res = cantonese_utils.jyutping_sound_changes(["deng?"])
        self.assertEqual(res, ["(d|t)eng?"])

    def test_t_initial(self):
        res = cantonese_utils.jyutping_sound_changes(["teng"])
        self.assertEqual(res, ["(d|t)eng"])

        res = cantonese_utils.jyutping_sound_changes(["teng1"])
        self.assertEqual(res, ["(d|t)eng1"])

        res = cantonese_utils.jyutping_sound_changes(["teng?"])
        self.assertEqual(res, ["(d|t)eng?"])

    def test_c(self):
        res = cantonese_utils.jyutping_sound_changes(["ceng"])
        self.assertEqual(res, ["(c|z)eng"])

        res = cantonese_utils.jyutping_sound_changes(["ceng1"])
        self.assertEqual(res, ["(c|z)eng1"])

        res = cantonese_utils.jyutping_sound_changes(["ceng?"])
        self.assertEqual(res, ["(c|z)eng?"])

    def test_z(self):
        res = cantonese_utils.jyutping_sound_changes(["zeng"])
        self.assertEqual(res, ["(c|z)eng"])

        res = cantonese_utils.jyutping_sound_changes(["zeng2"])
        self.assertEqual(res, ["(c|z)eng2"])

        res = cantonese_utils.jyutping_sound_changes(["zeng?"])
        self.assertEqual(res, ["(c|z)eng?"])

    def test_g(self):
        res = cantonese_utils.jyutping_sound_changes(["ging"])
        self.assertEqual(res, ["(g|k)ing"])

        res = cantonese_utils.jyutping_sound_changes(["ging1"])
        self.assertEqual(res, ["(g|k)ing1"])

        res = cantonese_utils.jyutping_sound_changes(["ging?"])
        self.assertEqual(res, ["(g|k)ing?"])

    def test_k_initial(self):
        res = cantonese_utils.jyutping_sound_changes(["king"])
        self.assertEqual(res, ["(g|k)ing"])

        res = cantonese_utils.jyutping_sound_changes(["king1"])
        self.assertEqual(res, ["(g|k)ing1"])

        res = cantonese_utils.jyutping_sound_changes(["king?"])
        self.assertEqual(res, ["(g|k)ing?"])

    def test_aa(self):
        res = cantonese_utils.jyutping_sound_changes(["mak"])
        self.assertEqual(res, ["maa!(k|t)"])

        res = cantonese_utils.jyutping_sound_changes(["mak6"])
        self.assertEqual(res, ["maa!(k|t)6"])

        res = cantonese_utils.jyutping_sound_changes(["mak?"])
        self.assertEqual(res, ["maa!(k|t)?"])

        res = cantonese_utils.jyutping_sound_changes(["maak"])
        self.assertEqual(res, ["maa!(k|t)"])

        res = cantonese_utils.jyutping_sound_changes(["maak1"])
        self.assertEqual(res, ["maa!(k|t)1"])

        res = cantonese_utils.jyutping_sound_changes(["maak?"])
        self.assertEqual(res, ["maa!(k|t)?"])

    def test_ang(self):
        res = cantonese_utils.jyutping_sound_changes(["maang"])
        self.assertEqual(res, ["maa!ng!"])

        res = cantonese_utils.jyutping_sound_changes(["maang4"])
        self.assertEqual(res, ["maa!ng!4"])

        res = cantonese_utils.jyutping_sound_changes(["maang?"])
        self.assertEqual(res, ["maa!ng!?"])

        res = cantonese_utils.jyutping_sound_changes(["mang"])
        self.assertEqual(res, ["maa!ng!"])

        res = cantonese_utils.jyutping_sound_changes(["mang1"])
        self.assertEqual(res, ["maa!ng!1"])

        res = cantonese_utils.jyutping_sound_changes(["mang?"])
        self.assertEqual(res, ["maa!ng!?"])

    def test_ong(self):
        res = cantonese_utils.jyutping_sound_changes(["bong"])
        self.assertEqual(res, ["bong!"])

        res = cantonese_utils.jyutping_sound_changes(["bong2"])
        self.assertEqual(res, ["bong!2"])

        res = cantonese_utils.jyutping_sound_changes(["bong?"])
        self.assertEqual(res, ["bong!?"])

    def test_an(self):
        res = cantonese_utils.jyutping_sound_changes(["maan"])
        self.assertEqual(res, ["maa!ng!"])

        res = cantonese_utils.jyutping_sound_changes(["maan4"])
        self.assertEqual(res, ["maa!ng!4"])

        res = cantonese_utils.jyutping_sound_changes(["maan?"])
        self.assertEqual(res, ["maa!ng!?"])

        res = cantonese_utils.jyutping_sound_changes(["man"])
        self.assertEqual(res, ["maa!ng!"])

        res = cantonese_utils.jyutping_sound_changes(["man1"])
        self.assertEqual(res, ["maa!ng!1"])

        res = cantonese_utils.jyutping_sound_changes(["man?"])
        self.assertEqual(res, ["maa!ng!?"])

    def test_on(self):
        res = cantonese_utils.jyutping_sound_changes(["mon"])
        self.assertEqual(res, ["mong!"])

        res = cantonese_utils.jyutping_sound_changes(["mon2"])
        self.assertEqual(res, ["mong!2"])

        res = cantonese_utils.jyutping_sound_changes(["mon?"])
        self.assertEqual(res, ["mong!?"])

    def test_t_final(self):
        res = cantonese_utils.jyutping_sound_changes(["got"])
        self.assertEqual(res, ["(g|k)w!o(k|t)"])

        res = cantonese_utils.jyutping_sound_changes(["got3"])
        self.assertEqual(res, ["(g|k)w!o(k|t)3"])

        res = cantonese_utils.jyutping_sound_changes(["got?"])
        self.assertEqual(res, ["(g|k)w!o(k|t)?"])

        res = cantonese_utils.jyutping_sound_changes(["bit"])
        self.assertEqual(res, ["bit"])

        res = cantonese_utils.jyutping_sound_changes(["bit6"])
        self.assertEqual(res, ["bit6"])

        res = cantonese_utils.jyutping_sound_changes(["bit?"])
        self.assertEqual(res, ["bit?"])

        res = cantonese_utils.jyutping_sound_changes(["but"])
        self.assertEqual(res, ["but"])

        res = cantonese_utils.jyutping_sound_changes(["but6"])
        self.assertEqual(res, ["but6"])

        res = cantonese_utils.jyutping_sound_changes(["but?"])
        self.assertEqual(res, ["but?"])

    def test_k_final(self):
        res = cantonese_utils.jyutping_sound_changes(["gok"])
        self.assertEqual(res, ["(g|k)w!o(k|t)"])

        res = cantonese_utils.jyutping_sound_changes(["gok3"])
        self.assertEqual(res, ["(g|k)w!o(k|t)3"])

        res = cantonese_utils.jyutping_sound_changes(["gok?"])
        self.assertEqual(res, ["(g|k)w!o(k|t)?"])

        res = cantonese_utils.jyutping_sound_changes(["bik"])
        self.assertEqual(res, ["bik"])

        res = cantonese_utils.jyutping_sound_changes(["bik6"])
        self.assertEqual(res, ["bik6"])

        res = cantonese_utils.jyutping_sound_changes(["bik?"])
        self.assertEqual(res, ["bik?"])

        res = cantonese_utils.jyutping_sound_changes(["buk"])
        self.assertEqual(res, ["buk"])

        res = cantonese_utils.jyutping_sound_changes(["buk1"])
        self.assertEqual(res, ["buk1"])

        res = cantonese_utils.jyutping_sound_changes(["buk?"])
        self.assertEqual(res, ["buk?"])


class TestJyutpingSegmentation(TestCase):
    def test_simple(self):
        _, res = cantonese_utils.segment_jyutping("m4 goi1")
        self.assertEqual(res, ["m4", "goi1"])

    def test_no_digits(self):
        _, res = cantonese_utils.segment_jyutping("m goi")
        self.assertEqual(res, ["m", "goi"])

    def test_no_spaces(self):
        _, res = cantonese_utils.segment_jyutping("m4goi1")
        self.assertEqual(res, ["m4", "goi1"])

    def test_no_digits_no_spaces(self):
        _, res = cantonese_utils.segment_jyutping("mgoi")
        self.assertEqual(res, ["m", "goi"])

    def test_no_digits_apostrophe(self):
        _, res = cantonese_utils.segment_jyutping("m'aam")
        self.assertEqual(res, ["m", "aam"])

    def test_digits_apostrophe(self):
        _, res = cantonese_utils.segment_jyutping("m4'aam")
        self.assertEqual(res, ["m4", "aam"])

    def test_remove_special_characters(self):
        _, res = cantonese_utils.segment_jyutping("m*goi")
        self.assertEqual(res, ["m", "goi"])

    def test_keep_glob_characters(self):
        _, res = cantonese_utils.segment_jyutping("m* goi", remove_glob_characters=False)
        self.assertEqual(res, ["m", "* ", "goi"])

    def test_keep_glob_characters_no_whitespace(self):
        _, res = cantonese_utils.segment_jyutping("m*goi", remove_glob_characters=False)
        self.assertEqual(res, ["m", "*", "goi"])

    def test_keep_multiple_glob_characters(self):
        _, res = cantonese_utils.segment_jyutping("m?* goi", remove_glob_characters=False)
        self.assertEqual(res, ["m", "?", "* ", "goi"])

    def test_keep_multiple_glob_characters_whitespace(self):
        _, res = cantonese_utils.segment_jyutping(
            "m? * goi", remove_glob_characters=False
        )
        self.assertEqual(res, ["m", "? ", "* ", "goi"])

    def test_keep_multiple_glob_characters_whitespace_surround(self):
        _, res = cantonese_utils.segment_jyutping(
            "m ? * goi", remove_glob_characters=False
        )
        self.assertEqual(res, ["m", " ? ", "* ", "goi"])

    def test_glob_characters_trim_whitespace(self):
        _, res = cantonese_utils.segment_jyutping(
            "m  ?            *      goi", remove_glob_characters=False
        )
        self.assertEqual(res, ["m", " ? ", "* ", "goi"])

    def test_keep_special_characters(self):
        _, res = cantonese_utils.segment_jyutping(
            "m？ goi", remove_special_characters=False
        )
        self.assertEqual(res, ["m", "？", "goi"])

    def test_remove_whitespace(self):
        _, res = cantonese_utils.segment_jyutping(
            "  m                           goi      "
        )
        self.assertEqual(res, ["m", "goi"])

    def test_lower(self):
        _, res = cantonese_utils.segment_jyutping("mGoI")
        self.assertEqual(res, ["m", "goi"])

    def test_lower_with_digits(self):
        _, res = cantonese_utils.segment_jyutping("m4GoI1")
        self.assertEqual(res, ["m4", "goi1"])

    def test_multiple_finals_vowels_only(self):
        _, res = cantonese_utils.segment_jyutping("aaaa")
        self.assertEqual(res, ["aa", "aa"])

    def test_multiple_finals_consonants_only(self):
        _, res = cantonese_utils.segment_jyutping("ngng")
        self.assertEqual(res, ["ng", "ng"])

    def test_multiple_finals(self):
        _, res = cantonese_utils.segment_jyutping("amam")
        self.assertEqual(res, ["am", "am"])

    def test_garbage(self):
        validity, res = cantonese_utils.segment_jyutping("kljnxclkjvnl")
        self.assertEqual(validity, False)
        self.assertEqual(res, ["kljnxclkjvnl"])


class TestFuzzyJyutping(TestCase):
    def test_clarence(self):
        cases = [("seut goh", ["s(eo|yu)(k|t)", "(g|k)w!ou"]),
                 ("gongyeun", ["(g|k)w!(o|u)ng", "j(eo|yu)n"]),
                 ("tsum4yut6", ["(c|z)aa!m4", "(jaa!|jyu|yu)(k|t)6"]),
                 ("tsum yut", ["(c|z)aa!m", "(jaa!|jyu|yu)(k|t)"]),
                 ("gum yut", ["(g|k)aa!m", "(jaa!|jyu|yu)(k|t)"]),
                 ("gum man", ["(g|k)aa!m", "maa!ng!"]),
                 ("sum", ["saa!m"]),
                 ("sun", ["s(y!u|aa!|eo)n"]),
                 ("cheung", ["(c|z)oeng"]),
                 ("chun", ["(c|z)(y!u|aa!|eo)n"]),
                 ("hui", ["heoi"]),
                 ("yutback", ["j(aa!|yu)(k|t)", "baa!(k|t)"])]

        for case in cases:
            input = case[0]
            expected_output = case[1]

            intermediate = cantonese_utils.jyutping_autocorrect(input)
            _, intermediate = cantonese_utils.segment_jyutping(intermediate, True, False, False)
            output = cantonese_utils.jyutping_sound_changes(intermediate)

            self.assertEqual(expected_output, output)

    def test_michelle(self):
        cases = [("xuet go", ["s(yu)(k|t)", "(g|k)w!o"]),
                 ("gong yuen", ["(g|k)w!(o|u)ng", "jy(y!u|aa!|eo)n"]),
                 ("kum yut", ["(g|k)aa!m", "(jaa!|jyu|yu)(k|t)"]),
                 ("gai suen gay", ["(g|k)aa!i", "s(yu)n", "(g|k)ei"]),
                 ("yut bak", ["j(aa!|yu)(k|t)", "baa!(k|t)"])]

        for case in cases:
            input = case[0]
            expected_output = case[1]

            intermediate = cantonese_utils.jyutping_autocorrect(input)
            _, intermediate = cantonese_utils.segment_jyutping(intermediate, True, False, False)
            output = cantonese_utils.jyutping_sound_changes(intermediate)

            self.assertEqual(expected_output, output)

    def test_yvonne(self):
        cases = [("shyut go", ["s(yu)(k|t)", "(g|k)w!o"]),
                 ("gong yun", ["(g|k)w!(o|u)ng", "(jaa!|jyu|yu)n"]),
                 ("cum yut", ["(k)aa!m", "(jaa!|jyu|yu)(k|t)"]),
                 ("cheun", ["(c|z)(eo|yu)n"]),
                 ("gai syun gei", ["(g|k)aa!i", "sy(y!u|aa!|eo)n", "(g|k)ei"]),
                 ("yut baat", ["j(aa!|yu)(k|t)", "baa!(k|t)"])]

        for case in cases:
            input = case[0]
            expected_output = case[1]

            intermediate = cantonese_utils.jyutping_autocorrect(input)
            _, intermediate = cantonese_utils.segment_jyutping(intermediate, True, False, False)
            output = cantonese_utils.jyutping_sound_changes(intermediate)

            self.assertEqual(expected_output, output)

    def test_other(self):
        cases = [("shut goh", ["s(aa!|y!u)(k|t)", "(g|k)w!ou"])]

        for case in cases:
            input = case[0]
            expected_output = case[1]

            intermediate = cantonese_utils.jyutping_autocorrect(input)
            _, intermediate = cantonese_utils.segment_jyutping(intermediate, True, False, False)
            output = cantonese_utils.jyutping_sound_changes(intermediate)

            self.assertEqual(expected_output, output)
