CREATE OR REPLACE FUNCTION public.tg_copy_to_pers_messages()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO public.pers_messages (id, sender, body, moment, account)
    VALUES (NEW.id, NEW.sender, NEW.body, NEW.moment, NEW.account);
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_after_insert_temp_messages
AFTER INSERT ON public.temp_messages
FOR EACH ROW
EXECUTE FUNCTION public.tg_copy_to_pers_messages();